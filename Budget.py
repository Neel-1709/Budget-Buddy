import google.generativeai as genai
import streamlit as st
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ============ Gemini Setup ============
genai.configure(api_key="AIzaSyDg-nYA54jfBUywmGoHR8Kvsirt5Z6GhEk")  # Replace with env var if deploying
llm_model = genai.GenerativeModel("gemini-2.5-flash")

# ============ Streamlit UI ============
st.title("💸 Budget Buddy: Your Smart Guide to Budgeting")

st.write("Answer the questions below to get a personalized financial plan and local resources from your AI financial advisor.")

# Collect user input
st.subheader("Basic Info")
st.write("Please fill out the information below to get personalized advice.")
name = st.text_input("Your Name")
age = st.text_input("Age")
region = st.text_input("City or Region")
dependents = st.text_input("How many dependents do you have?")

st.subheader("Income & Housing")
income = st.text_input("Monthly Net Income")
housing_type = st.selectbox("Do you rent or own?", ["Rent", "Own", "Live with Family"])
housing_cost = st.text_input("Monthly Rent / Mortgage")

st.subheader("Monthly Expenses")
utilities = st.text_input("Utilities (Electric, Internet, etc.)")
groceries = st.text_input("Groceries")
insurance = st.text_input("Insurance (Health, Car, etc.)")
transportation = st.text_input("Transportation (Fuel, Transit)")
other_expenses = st.text_input("Other Necessary Expenses")

st.subheader("Debt & Savings")
has_debt = st.selectbox("Do you have any debt?", ["Yes", "No"])
total_debt = st.text_input("Total Debt Amount") 
if has_debt == "No":
    total_debt = 0
monthly_debt_payment = st.text_input("Monthly Debt Payment")
if has_debt == "No":
    monthly_debt_payment = 0
current_savings = st.text_input("Current Savings")

st.subheader("Financial Goals")
goal = st.text_input("Main Goal (e.g., Save for a car)")

st.subheader("Other")
investments = st.text_input("Do you have any investments? If yes, describe them briefly:")
risk = st.selectbox("What is your risk tolerance?", ["Low", "Medium", "High"])
upcoming = st.text_input("Do you have any major upcoming expenses? (e.g., tuition, car, moving)")

# Button for budget advice
if st.button("Get Budget Advice"):
    inputs = [dependents, age, income, utilities, groceries, insurance, transportation, other_expenses, current_savings, investments, total_debt, monthly_debt_payment, goal, risk, region, upcoming]
    if not all(field.strip() for field in inputs):
        st.warning("Please fill out all fields.")
    else:
        prompt = f"""
        Act as a certified financial advisor. Use the information below to give a 
        tailored, professional budgeting analysis. 

        You are a certified financial advisor. Use the information below to provide a personalized, detailed budgeting and financial planning analysis.

        User Profile:
        - Number of Dependents: {dependents_val}
        - Age: {age_val}
        - Region/City: {region_val}
        - Monthly Net Income: ${income_val}

        Monthly Expenses Breakdown:
        - Utilities: ${utilities_val}
        - Groceries: ${groceries_val}
        - Insurance: ${insurance_val}
        - Transportation: ${transportation_val}
        - Other Necessary Expenses: ${other_expenses_val}
        - Total Monthly Expenses: ${total_expenses}

        Financial Overview:
        - Current Savings: ${current_savings_val}
        - Investments: {investments_val}
        - Total Debt: ${total_debt_val}
        - Monthly Debt Payment: ${monthly_debt_payment_val}

        Financial Goals and Preferences:
        - Primary Financial Goal: {goal_val}
        - Risk Tolerance: {risk_val}
        - Major Upcoming Expenses: {upcoming_val}

        Please organize your response into these sections:
        1. Summary of the User’s Current Financial Situation
        2. Customized Budgeting Recommendations, including saving, spending, and investing percentages
        3. Suggested Adjustments to improve financial health
        4. A 3-step Practical Action Plan the user can follow immediately
        5. Recommendations for Local or Free Financial Resources based on the region

        Provide clear, practical advice. If any critical information is missing or unclear, ask for clarification.
        """

        response = llm_model.generate_content(prompt)
        st.subheader("📊 Budget Buddy’s Advice:")
        st.write(response.parts[0].text if hasattr(response, "parts") else response.text)

# ============ Sidebar: Stock Investment Analyzer ============
st.sidebar.header("📈 Stock Investment Analyzer")

ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)")

if ticker:
    st.sidebar.write(f"Analyzing: **{ticker.upper()}**")

    try:
        # Fetch data from Yahoo Finance
        data = yf.download(ticker, start="2015-01-01", end=pd.Timestamp.today())
        data = data[['Close']].dropna()
        data['Previous Close'] = data['Close'].shift(1)
        data = data.dropna()

        # ======= Show Stock Graph in Sidebar =======
        st.sidebar.subheader("📉 Price Chart")
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(data.index, data['Close'], color='blue')
        ax.set_title(f"{ticker.upper()} Closing Prices")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.tick_params(axis='x', labelsize=6)
        ax.grid(True)
        st.sidebar.pyplot(fig)

        # ======= Prepare data for regression =======
        X = data[['Previous Close']]
        y = data['Close']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Linear Regression Model
        reg_model = LinearRegression()
        reg_model.fit(X_train, y_train)

        # Predict next day price
        last_close = float(data.iloc[-1]['Close'])
        predicted_next = float(reg_model.predict(pd.DataFrame([[last_close]], columns=["Previous Close"]))[0])

        # Show results
        st.sidebar.subheader("🔮 Prediction")
        st.sidebar.write(f"Last Close: **${last_close:.2f}**")
        st.sidebar.write(f"Predicted Next Day Close: **${predicted_next:.2f}**")

        if predicted_next > last_close:
            st.sidebar.success("✅ Suggestion: Consider investing. Trend shows growth.")
        else:
            st.sidebar.warning("⚠️ Suggestion: Hold off. Price may decrease or stay flat.")

    except Exception as e:
        st.sidebar.error(f"Error: {e}")