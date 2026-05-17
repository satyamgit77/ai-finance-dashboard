import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import sqlite3
import os
from google import genai  # Naya Gemini Client Import
import os
from dotenv import load_dotenv
load_dotenv() # Yeh line .env file se key ko load kar degi

# Page ki configuration
st.set_page_config(page_title="AI Finance Dashboard", layout="wide")

# Database folder banana agar nahi hai toh
if not os.path.exists("data"):
    os.makedirs("data")

DB_PATH = "data/finance.db"

# --- STEP 1: DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users Table banana
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT)''')
    # Transactions Table banana
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (transaction_id TEXT PRIMARY KEY, username TEXT, amount REAL, category TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- DATABASE FUNCTIONS ---
def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # Username pehle se exists karta hai
    conn.close()
    return success

def check_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_transaction_to_db(username, amount, category, date_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    tx_id = f"tx_{pd.Timestamp.now().timestamp()}"
    c.execute("INSERT INTO transactions (transaction_id, username, amount, category, date) VALUES (?, ?, ?, ?, ?)",
              (tx_id, username, amount, category, date_str))
    conn.commit()
    conn.close()

def load_user_data(username):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM transactions WHERE username=?", conn, params=(username,))
    conn.close()
    return df

# --- STEP 2: SESSION STATE FOR AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# --- STEP 3: LOGIN / SIGN UP WORKFLOW ---
if not st.session_state["logged_in"]:
    st.title("🔒 AI Finance Secure Portal")
    st.markdown("### Pehle apna Account Login karein ya Naya Account Banayein")
    
    tab1, tab2 = st.tabs(["🔐 Existing User? Login Here", "✨ New User? Sign Up Here"])
    
    with tab1:
        with st.form("login_form"):
            login_user = st.text_input("Username", key="l_user").strip()
            login_pass = st.text_input("Password", type="password", key="l_pass").strip()
            login_submit = st.form_submit_button("Login")
            
            if login_submit:
                if check_credentials(login_user, login_pass):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_user
                    st.success(f"Welcome back {login_user}! Logging in...")
                    st.rerun()
                else:
                    st.error("❌ Username nahi mila ya password galat hai! Agar naye ho toh Sign Up karo.")
                    
    with tab2:
        with st.form("signup_form"):
            st.info("💡 Apna naya unique username aur password chuniye")
            new_user = st.text_input("Choose Username", key="s_user").strip()
            new_pass = st.text_input("Choose Password", type="password", key="s_pass").strip()
            signup_submit = st.form_submit_button("Create Account & Sign Up")
            
            if signup_submit:
                if not new_user or not new_pass:
                    st.warning("⚠️ Dono fields bharna zaroori hai!")
                elif register_user(new_user, new_pass):
                    st.success(f"🎉 Username '{new_user}' successfully register ho gaya! Ab upar wale 'Login' section me jaakar login karein.")
                else:
                    st.error("❌ Ye Username pehle se kisi ne le rakha hai. Kuch aur naya try karo!")
                    
    st.stop()

# --- STEP 4: MAIN DASHBOARD (Sirf successfully login ke baad dikhega) ---

st.sidebar.write(f"👤 User: **{st.session_state['username']}**")
if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.rerun()

st.title("🤖 AI-Driven Personal Finance Dashboard")
st.markdown(f"Welcome **{st.session_state['username']}** bhai! Yeh aapka secure personalized space hai.")
st.write("---")

# --- DATA ENTRY FORM IN SIDEBAR ---
st.sidebar.header("➕ Add New Transaction")
with st.sidebar.form("transaction_form", clear_on_submit=True):
    new_amount = st.number_input("Amount (Expenses ko Minus (-) me likhein, Income ko Positive)", value=-100.0)
    new_category = st.selectbox("Category", options=["Food", "Shopping", "Entertainment", "Housing", "Utilities", "Income"])
    new_date = st.date_input("Transaction Date")
    submit_button = st.form_submit_button("Save to Database")

if submit_button:
    add_transaction_to_db(st.session_state["username"], new_amount, new_category, str(new_date))
    st.sidebar.success("💾 Data safely saved in SQL Database!")
    st.rerun()

# --- DATA PROCESSING FOR LOGGED IN USER ---
df_user = load_user_data(st.session_state["username"])

if df_user.empty:
    st.info("👋 Aapke account me abhi koi transaction nahi hai. Left sidebar se 2-3 kharche add karo taaki AI, charts aur Chatbot chal sakein!")
else:
    df_user["date"] = pd.to_datetime(df_user["date"])
    df_user["month"] = df_user["date"].dt.month
    
    expenses = df_user[df_user["amount"] < 0].copy()
    expenses["amount"] = expenses["amount"].abs()
    
    if expenses.empty:
        st.warning("💡 Aapne sirf Income add ki hai, AI ko train karne ke liye thode Expenses (Minus me) bhi add kijiye!")
    else:
        # UI Layout for Metrics & Charts
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📊 Quick Summary")
            total_spent = expenses["amount"].sum()
            total_tx = len(expenses)
            st.metric(label="Total Expenses Tracked", value=f"₹{total_spent:,.2f}")
            st.metric(label="Total Transactions", value=total_tx)
            
        with col2:
            st.subheader("🍔 Expense Distribution")
            cat_summary = expenses.groupby("category")["amount"].sum().reset_index()
            fig = px.pie(cat_summary, values="amount", names="category", hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)

        # AI PREDICTOR
        st.write("---")
        st.header("🔮 AI Expense Predictor")
        
        if len(expenses) >= 2:
            expenses["category_encoded"] = expenses["category"].astype("category").cat.codes
            X = expenses[["month", "category_encoded"]]
            y = expenses["amount"]
            
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X, y)
            cat_map = dict(zip(expenses["category"], expenses["category_encoded"]))
            
            col3, col4 = st.columns(2)
            with col3:
                selected_month = st.selectbox("Mahina chunye:", options=[1,2,3,4,5,6,7,8,9,10,11,12], index=5)
            with col4:
                selected_cat = st.selectbox("Category chunye:", options=list(cat_map.keys()))
                
            if st.button("🔮 Predict Future Expense", type="primary"):
                cat_code = cat_map[selected_cat]
                input_data = pd.DataFrame([[selected_month, cat_code]], columns=["month", "category_encoded"])
                prediction = model.predict(input_data)[0]
                st.success(f"🤖 AI Prediction: Month {selected_month} me **{selected_cat}** par lagbhag **₹{prediction:,.2f}** kharcha ho sakta hai!")
        else:
            st.warning("🤖 AI ko seekhne ke liye kam se kam 2 ya usse zyada expenses data chahiye.")

        # --- STEP 5: ASLI GEMINI AI CHATBOT SECTION (UPDATED) ---
        st.write("---")
        st.header("💬 AI Financial Chatbot (Gemini Powered)")
        st.markdown("Apne financial data se jude koi bhi sawaal poochhein. Gemini aapka live database padh kar jawab dega!")

        # ⚠️ YAHAN APNI GEMINI KEY PASTE KARNA ⚠️
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if GEMINI_API_KEY == "TUMHARI_GEMINI_API_KEY_YAHAN_PASTE_KARO":
            st.warning("🔑 Chatbot chalane ke liye pehle code ki line number 165 me apni asli Gemini API Key paste karein bhai!")
        else:
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                if "chat_history" not in st.session_state:
                    st.session_state["chat_history"] = [{"role": "assistant", "content": f"Hello {st.session_state['username']} bhai! Main Gemini AI Financial Assistant hoon. Aaj aapne expense ke bare me kya puchhna chahte hai?"}]

                for message in st.session_state["chat_history"]:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

                user_query = st.chat_input("Ask anything about your money...")

                if user_query:
                    with st.chat_message("user"):
                        st.write(user_query)
                    st.session_state["chat_history"].append({"role": "user", "content": user_query})
                    
                    # Database ko text (string) me badalna taaki Gemini padh sake
                    user_data_summary = df_user.to_string(index=False)
                    
                    system_prompt = f"""
                    You are a highly intelligent Indian personal finance guru who speaks in a friendly mix of Hindi and English (Hinglish).
                    You have direct secure access to the user's live SQL database transactions.
                    
                    Here is the real-time financial database of the user logged in ({st.session_state['username']}):
                    {user_data_summary}
                    
                    Strictly analyze this data and answer the user's question. If they ask about totals, averages, or specific categories, calculate it using the provided text database. 
                    Be smart, give savings tips if asked, and use 'bhai' occasionally. Keep answers concise.
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"{system_prompt}\n\nUser Question: {user_query}"
                    )
                    
                    bot_response = response.text
                    
                    with st.chat_message("assistant"):
                        st.write(bot_response)
                    st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"⚠️ Gemini API connect karne me dikkat aa rahi hai. Error: {e}")