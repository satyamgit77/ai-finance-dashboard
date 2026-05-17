# 💰 AI-Powered Personal Finance Dashboard

An intelligent Personal Finance Tracker application designed to help users seamlessy monitor their daily expenses and income. Powered by Machine Learning for expense forecasting and Google's Gemini AI for personalized financial insights.

## 🚀 Key Features

- **🔐 Secure User Authentication:** A custom Signup and Login system powered by a local SQLite database.
- **📊 Interactive Data Visualizations:** Beautiful, dynamic charts created using Plotly and Pandas to analyze spending patterns.
- **🤖 Gemini AI Financial Chatbot:** An integrated smart assistant that securely reads user transaction data to provide real-time budget advice.
- **🔒 Secure API Management:** Keeps sensitive API keys hidden locally using `.env` environment variables (protected via `.gitignore`).
- **🔮 Expense Predictor:** Built-in prediction capabilities using Scikit-Learn to forecast upcoming monthly expenses.

## 🛠️ Tech Stack

- **Python** (Core Logic)
- **Streamlit** (Web Interface & Dashboard)
- **SQLite3** (Database Management)
- **Google Gemini API (`google-genai`)** (LLM Integration)
- **Plotly & Pandas** (Data Analytics & Visualization)
- **Scikit-Learn** (Machine Learning Model)

## 💻 Local Installation & Setup

Follow these simple steps to get this project running on your computer:

### 1. Clone the Repository
Download or clone this project folder to your local machine.

### 2. Install Required Dependencies
Open your terminal inside the project directory and run:
```bash
pip install -r requirements.txt