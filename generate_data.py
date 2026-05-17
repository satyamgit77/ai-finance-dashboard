import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

NUM_USERS = 5
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 5, 25)

categories = {
    "Income": ["Salary", "Freelance", "Investment Dividend"],
    "Housing": ["Rent", "Mortgage", "Electric Bill", "Water Bill"],
    "Food": ["Whole Foods", "Trader Joe's", "Kroger", "McDonalds", "Starbucks", "Local Restaurant"],
    "Transportation": ["Gas Station", "Uber", "Lyft", "Public Transit"],
    "Entertainment": ["Netflix", "Spotify", "Movie Theater", "Concert Ticket"],
    "Shopping": ["Amazon", "Target", "Walmart", "Clothing Store"]
}

def generate_financial_data():
    users = []
    accounts = []
    transactions = []

    for _ in range(NUM_USERS):
        user_id = str(uuid.uuid4())

        user_profile = {
            "user_id": user_id,
            "name": fake.name(),
            "email": fake.email(),
            "risk_tolerance": random.choice(["Low", "Medium", "High"]),
            "created_at": START_DATE
        }
        users.append(user_profile)

        # Create a Checking and Savings account for each user
        checking_id = str(uuid.uuid4())
        savings_id = str(uuid.uuid4())

        accounts.append({
            "account_id": checking_id,
            "user_id": user_id,
            "account_type": "Checking",
            "balance": 2500.00
        })
        accounts.append({
            "account_id": savings_id,
            "user_id": user_id,
            "account_type": "Savings",
            "balance": 10000.00
        })

        # Generate Transactions over time
        current_date = START_DATE
        while current_date <= END_DATE:

            # 1. Monthly Salary (1st of the month)
            if current_date.day == 1:
                transactions.append({
                    "transaction_id": str(uuid.uuid4()),
                    "account_id": checking_id,
                    "amount": 4500.00,
                    "merchant": random.choice(categories["Income"]),
                    "category": "Income",
                    "timestamp": current_date.replace(hour=9, minute=0)
                })

                # 2. Monthly Rent (2nd of the month)
            if current_date.day == 2:
                transactions.append({
                    "transaction_id": str(uuid.uuid4()),
                    "account_id": checking_id,
                    "amount": -1200.00,
                    "merchant": "Rent Payment",
                    "category": "Housing",
                    "timestamp": current_date.replace(hour=10, minute=0)
                })

                # 3. Daily Random Expenses (Food, Shopping, Uber etc.)
            # Hum chahte hain ki roz 1 se 3 random kharche hon
            num_expenses = random.randint(1, 3)
            
            for _ in range(num_expenses):
                # Income ko chhod kar koi bhi ek random expense category chunenge
                available_categories = [cat for cat in categories.keys() if cat != "Income"]
                chosen_category = random.choice(available_categories)
                chosen_merchant = random.choice(categories[chosen_category])
                
                # Kharcha random hoga ₹5 se ₹150 ke beech me
                expense_amount = round(random.uniform(5.0, 150.0), 2)
                
                # Random time (subah 8 baje se raat 10 baje ke beech)
                random_hour = random.randint(8, 22)
                random_minute = random.randint(0, 59)

                transactions.append({
                    "transaction_id": str(uuid.uuid4()),
                    "account_id": checking_id,
                    "amount": -expense_amount, # Minus kyunki kharcha hai
                    "merchant": chosen_merchant,
                    "category": chosen_category,
                    "timestamp": current_date.replace(hour=random_hour, minute=random_minute)
                })
                # Tarikh ko 1 din aage badhayenge taaki loop chalta rahe
            current_date += timedelta(days=1)

    return users, accounts, transactions
    
    
# Function ko call karke data generate kar rahe hain
u_data, a_data, t_data = generate_financial_data()

# Test karne ke liye pehle user ka data print karke dekhte hain
print("--- TEST RUN SUCCESSFUL ---")
print(f"Total Users Generated: {len(u_data)}")
print(f"Total Accounts Generated: {len(a_data)}")
print(f"Total Transactions Generated: {len(t_data)}")
print("\nPehle User Ki Detail:")
print(u_data[0])

# Data ko DataFrames me badal rahe hain
df_users = pd.DataFrame(u_data)
df_accounts = pd.DataFrame(a_data)
df_transactions = pd.DataFrame(t_data)

# Data ko CSV files me save kar rahe hain
df_users.to_csv("data/users.csv", index=False)
df_accounts.to_csv("data/accounts.csv", index=False)
df_transactions.to_csv("data/transactions.csv", index=False)

print("\n--- ALL DATA SAVED TO CSV SUCCESSFULLY ---")