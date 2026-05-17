import sqlite3
import pandas as pd

# Database se connect karein
conn = sqlite3.connect("data/finance.db")

print("--- USERS TABLE ---")
df_users = pd.read_sql_query("SELECT * FROM users", conn)
print(df_users)

print("\n--- TRANSACTIONS TABLE ---")
df_tx = pd.read_sql_query("SELECT * FROM transactions", conn)
print(df_tx)

conn.close()