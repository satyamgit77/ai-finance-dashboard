import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="FinSight AI | Personal Finance",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================
st.markdown("""
<style>
    :root {
        --rzp-blue: #2b84ea;
        --rzp-blue-dark: #1769c2;
        --rzp-navy: #0b1f33;
        --rzp-bg: #f4f8fc;
        --rzp-border: #dce7f2;
        --rzp-text: #172b4d;
        --rzp-muted: #66788a;
        --rzp-white: #ffffff;
    }

    * { box-sizing: border-box; }

    .stApp {
        background: linear-gradient(180deg, #f7faff 0%, #f3f7fb 100%);
        color: var(--rzp-text);
    }

    .main .block-container {
        max-width: 1500px;
        padding: 1.5rem 2.5rem 3rem;
    }

    /* ================= SIDEBAR ================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1f33 0%, #123b66 100%);
        border-right: 0;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1.25rem 1rem 2rem;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.16);
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #b9cbe0 !important;
    }

    [data-testid="stSidebar"] label p {
        color: #eaf3ff !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background: rgba(255,255,255,.08) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,.18) !important;
    }

    [data-testid="stSidebar"] input::placeholder {
        color: #a9bdd3 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,.08) !important;
        border-color: rgba(255,255,255,.18) !important;
        color: white !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }

    [data-testid="stSidebar"] .stNumberInput button {
        background: rgba(255,255,255,.08) !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,.09) !important;
        border: 1px solid rgba(255,255,255,.18) !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,.17) !important;
        border-color: rgba(255,255,255,.35) !important;
    }

    [data-testid="stSidebar"] .stFormSubmitButton > button {
        background: linear-gradient(135deg, #2b84ea, #1769c2) !important;
        border: 0 !important;
        color: white !important;
        box-shadow: 0 7px 18px rgba(0,0,0,.18);
    }

    /* ================= BRAND ================= */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 6px 5px 2px;
    }

    .brand-mark {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #2b84ea, #58a8ff);
        box-shadow: 0 8px 22px rgba(43,132,234,.28);
        font-size: 21px;
    }

    .brand-name {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -.4px;
        color: white;
    }

    .brand-tag {
        font-size: 11px;
        color: #b9cbe0;
        margin-top: -2px;
    }

    /* ================= DASHBOARD ================= */
    .hero {
        background: linear-gradient(135deg, #0b1f33 0%, #164e82 55%, #2b84ea 100%);
        padding: 30px 34px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 16px 38px rgba(22,78,130,.16);
        overflow: hidden;
        position: relative;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -80px;
        top: -90px;
        border-radius: 50%;
        background: rgba(255,255,255,.08);
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(25px, 3vw, 36px);
        font-weight: 800;
        letter-spacing: -.8px;
    }

    .hero p {
        margin: 8px 0 0;
        color: #dbeeff;
        font-size: 15px;
        line-height: 1.6;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: var(--rzp-navy);
        margin-top: 20px;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: var(--rzp-muted);
        margin-bottom: 18px;
        font-size: 14px;
    }

    /* ================= METRICS ================= */
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 17px;
        border: 1px solid var(--rzp-border);
        box-shadow: 0 8px 24px rgba(11,31,51,.055);
        min-height: 118px;
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(11,31,51,.09);
    }

    .metric-label {
        color: var(--rzp-muted);
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .metric-value {
        color: var(--rzp-navy);
        font-size: clamp(22px, 2.2vw, 30px);
        font-weight: 800;
        margin-top: 9px;
        word-break: break-word;
    }

    /* ================= CARDS ================= */
    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid var(--rzp-border);
        height: 100%;
        box-shadow: 0 8px 24px rgba(11,31,51,.05);
    }

    .feature-card h4 {
        margin-top: 0;
        color: var(--rzp-navy);
    }

    .feature-card p {
        color: var(--rzp-muted);
        font-size: 14px;
        line-height: 1.65;
    }

    /* ================= FORMS ================= */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        border-radius: 10px !important;
        border: 1px solid var(--rzp-border) !important;
        min-height: 43px;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stDateInput input:focus {
        border-color: var(--rzp-blue) !important;
        box-shadow: 0 0 0 2px rgba(43,132,234,.12) !important;
    }

    [data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: var(--rzp-border) !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px !important;
        min-height: 43px;
        font-weight: 700;
        transition: all .2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
    }

    /* Primary Streamlit buttons */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2b84ea, #1769c2) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 7px 18px rgba(43,132,234,.2);
    }

    /* ================= LOGIN ================= */
    .login-page {
        min-height: 80vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .login-card {
        background: rgba(255,255,255,.98);
        padding: 32px;
        border-radius: 24px;
        border: 1px solid var(--rzp-border);
        box-shadow: 0 20px 60px rgba(11,31,51,.10);
        margin-bottom: 14px;
    }

    .login-brand {
        text-align: center;
        margin-bottom: 25px;
    }

    .login-logo {
        width: 58px;
        height: 58px;
        margin: 0 auto 13px;
        border-radius: 17px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #2b84ea, #1769c2);
        color: white;
        font-size: 28px;
        box-shadow: 0 10px 26px rgba(43,132,234,.22);
    }

    .login-title {
        color: var(--rzp-navy);
        font-size: 29px;
        font-weight: 850;
        letter-spacing: -.7px;
    }

    .login-subtitle {
        color: var(--rzp-muted);
        font-size: 14px;
        margin-top: 5px;
    }

    /* ================= CHAT ================= */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        border: 1px solid var(--rzp-border);
        background: white;
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    /* ================= TABLE / ALERTS ================= */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--rzp-border);
        border-radius: 14px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    footer { visibility: hidden; }

    /* ================= RESPONSIVE ================= */
    @media (max-width: 900px) {
        .main .block-container {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 24px;
            border-radius: 17px;
        }

        .metric-card {
            min-height: 105px;
            padding: 16px;
        }

        .metric-value {
            font-size: 22px;
        }

        .login-card {
            padding: 22px;
            border-radius: 18px;
        }
    }

    @media (max-width: 600px) {
        .main .block-container {
            padding: .75rem .75rem 2rem;
        }

        .hero h1 {
            font-size: 25px;
        }

        .hero p {
            font-size: 13px;
        }

        .section-title {
            font-size: 20px;
        }

        .login-card {
            padding: 18px;
        }

        .login-title {
            font-size: 25px;
        }
    }

    /* Fintech accent elements */
    .stRadio > div {
        gap: 8px;
    }

    .stRadio label {
        border-radius: 10px;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        box-shadow: 0 8px 25px rgba(11,31,51,.045);
    }

    /* Tabs on authentication */
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2b84ea !important;
    }

    /* Mobile sidebar / content spacing */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] .block-container {
            padding-left: .8rem;
            padding-right: .8rem;
        }

        .hero {
            margin-bottom: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DB_PATH = os.path.join(DATA_DIR, "finance.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            username TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================================
# DATABASE FUNCTIONS
# =========================================================
def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False

    conn.close()
    return success


def check_credentials(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()
    return user is not None


def add_transaction_to_db(username, amount, category, date_str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    tx_id = f"tx_{pd.Timestamp.now().timestamp()}"

    c.execute(
        """
        INSERT INTO transactions
        (transaction_id, username, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (tx_id, username, amount, category, date_str)
    )

    conn.commit()
    conn.close()


def load_user_data(username):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM transactions WHERE username=?",
        conn,
        params=(username,)
    )

    conn.close()
    return df


# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""


# =========================================================
# LOGIN / SIGN UP
# =========================================================
if not st.session_state["logged_in"]:

    left, center, right = st.columns([0.7, 2.0, 0.7])

    with center:
        st.markdown("""
        <div class="login-card">
            <div class="login-brand">
                <div class="login-logo">💼</div>
                <div class="login-title">FinSight AI</div>
                <div class="login-subtitle">
                    Smart personal finance management with AI-powered insights.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            st.markdown("### Welcome back")
            st.caption("Sign in to access your personal finance dashboard.")

            with st.form("login_form"):
                login_user = st.text_input(
                    "Username",
                    placeholder="Enter your username"
                ).strip()

                login_pass = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                ).strip()

                login_submit = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary"
                )

            if login_submit:
                if check_credentials(login_user, login_pass):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_user
                    st.success("Login successful. Loading your dashboard...")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")

        with tab2:
            st.markdown("### Create your account")
            st.caption("Start tracking your finances in one secure dashboard.")

            with st.form("signup_form"):
                new_user = st.text_input(
                    "Choose Username",
                    placeholder="Create a username"
                ).strip()

                new_pass = st.text_input(
                    "Choose Password",
                    type="password",
                    placeholder="Create a password"
                ).strip()

                signup_submit = st.form_submit_button(
                    "Create Account",
                    use_container_width=True,
                    type="primary"
                )

            if signup_submit:
                if not new_user or not new_pass:
                    st.warning("Please complete both fields.")
                elif register_user(new_user, new_pass):
                    st.success(
                        f"Account '{new_user}' created successfully. "
                        "Please sign in to continue."
                    )
                else:
                    st.error(
                        "That username is already in use. Please choose another."
                    )

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================
username = st.session_state["username"]

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-mark">💼</div>
        <div>
            <div class="brand-name">FinSight AI</div>
            <div class="brand-tag">Personal Finance Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 👤 Account")
    st.markdown(f"**{username}**")

    st.divider()

    st.markdown("### ➕ Add Transaction")

    with st.form("transaction_form", clear_on_submit=True):
        transaction_type = st.radio(
            "Transaction Type",
            options=["Expense", "Income"],
            horizontal=True
        )

        new_amount = st.number_input(
            "Amount",
            min_value=0.0,
            value=100.0,
            step=50.0,
            help="Enter the amount as a positive number."
        )

        if transaction_type == "Expense":
            new_category = st.selectbox(
                "Expense Category",
                options=[
                    "Food",
                    "Shopping",
                    "Entertainment",
                    "Housing",
                    "Utilities",
                    "Other"
                ]
            )
        else:
            new_category = "Income"
            st.caption("Income is automatically categorized as Income.")

        new_date = st.date_input("Transaction Date")

        submit_button = st.form_submit_button(
            "Save Transaction",
            use_container_width=True,
            type="primary"
        )

    if submit_button:
        # Expenses are stored as negative values internally so all existing
        # analytics/model logic continues to work. The user never needs to
        # enter a minus sign.
        stored_amount = -abs(new_amount) if transaction_type == "Expense" else abs(new_amount)

        if new_amount <= 0:
            st.warning("Please enter an amount greater than zero.")
        else:
            add_transaction_to_db(
                username,
                stored_amount,
                new_category,
                str(new_date)
            )
            st.success("Transaction saved successfully.")
            st.rerun()

    st.divider()

    if st.button("Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state.pop("chat_history", None)
        st.rerun()


# =========================================================
# MAIN DASHBOARD
# =========================================================
st.markdown(f"""
<div class="hero">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="
            width:48px;height:48px;border-radius:14px;
            display:flex;align-items:center;justify-content:center;
            background:rgba(255,255,255,.14);
            border:1px solid rgba(255,255,255,.18);
            font-size:25px;
        ">💼</div>
        <div>
            <div style="
                font-size:14px;font-weight:700;letter-spacing:.8px;
                color:#bfe0ff;text-transform:uppercase;
            ">FinSight AI</div>
            <div style="font-size:12px;color:#a9c8e6;">
                Intelligent Personal Finance
            </div>
        </div>
    </div>
    <h1>Financial Command Center</h1>
    <p>
        Welcome back, <strong>{username}</strong>.
        Track your money, understand your spending, and make smarter financial decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# Load user data
df_user = load_user_data(username)

if df_user.empty:
    st.info(
        "Your dashboard is ready. Add a few transactions from the sidebar "
        "to unlock analytics, predictions, and the AI financial assistant."
    )

    st.markdown("### What you can do")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Track Spending</h4>
            <p>
                Record your income and expenses and monitor your financial
                activity from one dashboard.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔮 Predict Expenses</h4>
            <p>
                Use the machine-learning predictor to estimate future
                category-level expenses.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 Ask AI</h4>
            <p>
                Ask questions about your financial activity and receive
                personalized AI-generated insights.
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    df_user["date"] = pd.to_datetime(df_user["date"])
    df_user["month"] = df_user["date"].dt.month

    expenses = df_user[df_user["amount"] < 0].copy()
    expenses["amount"] = expenses["amount"].abs()

    income_df = df_user[df_user["amount"] > 0].copy()

    # =====================================================
    # OVERVIEW
    # =====================================================
    st.markdown(
        '<div class="section-title">Financial Overview</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">A quick snapshot of your current activity.</div>',
        unsafe_allow_html=True
    )

    total_spent = expenses["amount"].sum() if not expenses.empty else 0
    total_income = income_df["amount"].sum() if not income_df.empty else 0
    total_tx = len(df_user)
    net_balance = total_income - total_spent

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Total Income</div>'
            f'<div class="metric-value">₹{total_income:,.2f}</div></div>',
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Total Expenses</div>'
            f'<div class="metric-value">₹{total_spent:,.2f}</div></div>',
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Net Balance</div>'
            f'<div class="metric-value">₹{net_balance:,.2f}</div></div>',
            unsafe_allow_html=True
        )

    with m4:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Transactions</div>'
            f'<div class="metric-value">{total_tx}</div></div>',
            unsafe_allow_html=True
        )

    st.write("")

    # =====================================================
    # ANALYTICS
    # =====================================================
    if expenses.empty:
        st.warning(
            "No expense transactions have been recorded yet. "
            "Add an expense using a negative amount to view spending analytics."
        )
    else:
        st.markdown(
            '<div class="section-title">Spending Analytics</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-subtitle">Understand where your money is going.</div>',
            unsafe_allow_html=True
        )

        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            cat_summary = (
                expenses.groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values("amount", ascending=False)
            )

            fig = px.pie(
                cat_summary,
                values="amount",
                names="category",
                hole=0.55,
                title="Expense Distribution"
            )

            fig.update_layout(
                margin=dict(t=60, l=10, r=10, b=10),
                legend_title_text="Category"
            )

            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            monthly_summary = (
                expenses.assign(month_name=expenses["date"].dt.strftime("%b"))
                .groupby(["month", "month_name"])["amount"]
                .sum()
                .reset_index()
                .sort_values("month")
            )

            fig2 = px.bar(
                monthly_summary,
                x="month_name",
                y="amount",
                title="Monthly Spending",
                labels={
                    "month_name": "Month",
                    "amount": "Expense (₹)"
                }
            )

            fig2.update_layout(
                margin=dict(t=60, l=10, r=10, b=10)
            )

            st.plotly_chart(fig2, use_container_width=True)

        # =================================================
        # RECENT TRANSACTIONS
        # =================================================
        st.markdown(
            '<div class="section-title">Recent Transactions</div>',
            unsafe_allow_html=True
        )

        display_df = df_user.sort_values("date", ascending=False).copy()
        display_df["Amount"] = display_df["amount"].apply(
            lambda x: f"+ ₹{x:,.2f}" if x > 0 else f"- ₹{abs(x):,.2f}"
        )
        display_df["Date"] = display_df["date"].dt.strftime("%d %b %Y")

        st.dataframe(
            display_df[
                ["Date", "category", "Amount"]
            ].rename(columns={
                "category": "Category"
            }),
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # AI EXPENSE PREDICTOR
        # =================================================
        st.divider()

        st.markdown(
            '<div class="section-title">🔮 AI Expense Predictor</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-subtitle">'
            'Estimate a future expense using the available transaction history.'
            '</div>',
            unsafe_allow_html=True
        )

        if len(expenses) >= 2:
            expenses["category_encoded"] = (
                expenses["category"].astype("category").cat.codes
            )

            X = expenses[["month", "category_encoded"]]
            y = expenses["amount"]

            model = RandomForestRegressor(
                n_estimators=50,
                random_state=42
            )
            model.fit(X, y)

            cat_map = dict(
                zip(
                    expenses["category"],
                    expenses["category_encoded"]
                )
            )

            p1, p2 = st.columns(2)

            with p1:
                selected_month = st.selectbox(
                    "Select Month",
                    options=list(range(1, 13)),
                    index=5,
                    format_func=lambda x: pd.Timestamp(
                        2026, x, 1
                    ).strftime("%B")
                )

            with p2:
                selected_cat = st.selectbox(
                    "Select Expense Category",
                    options=list(cat_map.keys())
                )

            if st.button(
                "Generate Expense Prediction",
                type="primary",
                use_container_width=True
            ):
                cat_code = cat_map[selected_cat]

                input_data = pd.DataFrame(
                    [[selected_month, cat_code]],
                    columns=["month", "category_encoded"]
                )

                prediction = model.predict(input_data)[0]

                st.success(
                    f"Estimated {selected_cat} expense: "
                    f"₹{prediction:,.2f}"
                )
        else:
            st.warning(
                "Add at least two expense transactions to enable the AI predictor."
            )

        # =================================================
        # GEMINI AI ASSISTANT
        # =================================================
        st.divider()

        st.markdown(
            '<div class="section-title">🤖 AI Financial Assistant</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-subtitle">'
            'Ask questions about your transactions and receive personalized financial insights.'
            '</div>',
            unsafe_allow_html=True
        )

        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        if not GEMINI_API_KEY:
            st.warning(
                "Gemini AI is not configured yet. Add GEMINI_API_KEY to your .env file "
                "to enable the AI Financial Assistant."
            )
        else:
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)

                if "chat_history" not in st.session_state:
                    st.session_state["chat_history"] = [
                        {
                            "role": "assistant",
                            "content": (
                                f"Hello {username}! I'm your AI Financial Assistant. "
                                "Ask me anything about your spending, income, or transactions."
                            )
                        }
                    ]

                for message in st.session_state["chat_history"]:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

                user_query = st.chat_input(
                    "Ask about your finances..."
                )

                if user_query:
                    with st.chat_message("user"):
                        st.write(user_query)

                    st.session_state["chat_history"].append({
                        "role": "user",
                        "content": user_query
                    })

                    user_data_summary = df_user.to_string(index=False)

                    system_prompt = f"""
You are an intelligent personal finance assistant.

The user is using an Indian personal finance dashboard.
Respond in clear, professional English.

You have access to the user's transaction data below.

User: {username}

Transaction data:
{user_data_summary}

Instructions:
- Analyze only the provided transaction data when answering questions about the user's finances.
- Calculate totals, averages, categories, and other requested values carefully.
- Give practical and responsible financial suggestions when appropriate.
- Do not invent transactions or financial facts.
- Keep answers concise, useful, and easy to understand.
"""

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=(
                            f"{system_prompt}\n\n"
                            f"User Question: {user_query}"
                        )
                    )

                    bot_response = response.text

                    with st.chat_message("assistant"):
                        st.write(bot_response)

                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": bot_response
                    })

            except Exception as e:
                st.error(
                    f"Unable to connect to the Gemini AI service. Error: {e}"
                )
