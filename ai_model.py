import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. CSV Data ko load karna
df = pd.read_csv("data/transactions.csv")

# 2. Sirf kharchon (Expenses) par focus karna, income ko hata dena
df_expenses = df[df["amount"] < 0].copy()

# 3. Amount ko positive kar dena taaki calculation me aasaani ho
df_expenses["amount"] = df_expenses["amount"].abs()

# 4. Tarikh me se Mahina (Month) nikalna
df_expenses["timestamp"] = pd.to_datetime(df_expenses["timestamp"])
df_expenses["month"] = df_expenses["timestamp"].dt.month

print("--- RAW DATA LOADED FOR AI ---")
print(df_expenses.head())

# 5. Data ko Group karna (User + Month + Category ke hisab se total kharcha)
features_df = df_expenses.groupby(["month", "category"])["amount"].sum().reset_index()

# 6. Category ko numbers me badalna (AI text nahi samajhta, numbers samajhta hai)
features_df["category_encoded"] = features_df["category"].astype("category").cat.codes

print("\n--- AI-READY SUMMARY TABLE ---")
print(features_df.head(10))

# 7. Sawaal (X) aur Jawaab (y) ko alag karna
X = features_df[["month", "category_encoded"]] # Features
y = features_df["amount"]                       # Target

# 8. Data ko Train aur Test sets me baantna (80% Padhai, 20% Exam)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n--- DATA SPLIT FOR TRAINING ---")
print(f"Training Sawaal (X_train) Rows: {X_train.shape[0]}")
print(f"Testing Sawaal (X_test) Rows: {X_test.shape[0]}")

# 9. AI Model (Dimaag) ko taiyar karna
model = RandomForestRegressor(n_estimators=100, random_state=42)

# 10. AI ki padhai shuru (Training the model)
print("\nAI Model ki training shuru ho rahi hai...")
model.fit(X_train, y_train)
print("AI Model successfully train ho gaya!")

# 11. AI ka Exam (Testing on unseen data)
y_pred = model.predict(X_test)

# 12. Report Card nikalna (Galti check karna)
mae = mean_absolute_error(y_test, y_pred)
print(f"\nModel Ka Report Card (Mean Absolute Error): ₹{mae:.2f}")

print("\n--- MAKING A FUTURE PREDICTION ---")

# Ek naya test case banate hain:
# Mahina = 6 (June), Category_Encoded = 5 (Shopping)
naya_sawaal = pd.DataFrame([[6, 5]], columns=["month", "category_encoded"])

# AI se prediction maang rahe hain
future_expense = model.predict(naya_sawaal)

print(f"AI Prediction: June ke mahine me Shopping par lagbhag ₹{future_expense[0]:.2f} kharcha hoga!")