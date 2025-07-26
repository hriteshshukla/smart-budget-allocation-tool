import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------
# Define allocation logic and thresholds
# ----------------------
def get_allocation(income, profile):
    if profile == "Student":
        essentials_pct, savings_pct, investments_pct = 0.70, 0.05, 0.00
        rent_max, food_max = 650, 180
    elif profile == "Graduate":
        essentials_pct, savings_pct, investments_pct = 0.60, 0.15, 0.10
        rent_max, food_max = 1000, 250
    elif profile == "Tier 2 Skilled Worker":
        essentials_pct, savings_pct, investments_pct = 0.55, 0.20, 0.15
        rent_max, food_max = 1200, 300
    else:
        essentials_pct, savings_pct, investments_pct = 0.60, 0.10, 0.05
        rent_max, food_max = 800, 200

    discretionary_pct = 1 - (essentials_pct + savings_pct + investments_pct)

    return {
        "Essentials": income * essentials_pct,
        "Savings": income * savings_pct,
        "Investments": income * investments_pct,
        "Discretionary": income * discretionary_pct
    }, rent_max, food_max

# ----------------------
# Streamlit App
# ----------------------
st.set_page_config(page_title="Smart Budget Allocation Tool", layout="centered")
st.title("📊 Smart Budget Allocation Tool")
st.markdown("""
Use this tool to get a personalised income allocation recommendation based on your profile and monthly income.

### How to Use:
1. Enter your **monthly income** in pounds.
2. Select the **user profile** that best describes your situation.
3. Click **"Generate My Budget Plan"** to view your recommended allocations.
4. A table and pie chart will show how to best divide your income.
""")

# Inputs
income = st.number_input("Enter your monthly income (£):", min_value=100, max_value=10000, value=1200)
profile = st.selectbox("Select your profile:", ["Student", "Graduate", "Tier 2 Skilled Worker", "Other"])
rent_input = st.number_input("Your current rent (£ per month):", min_value=0, max_value=5000, value=600)
food_input = st.number_input("Your current food + takeaway expenses (£ per month):", min_value=0, max_value=2000, value=150)

# Calculate and Display Results
if st.button("Generate My Budget Plan"):
    allocation, rent_max, food_max = get_allocation(income, profile)
    df_alloc = pd.DataFrame.from_dict(allocation, orient='index', columns=['Amount (£)'])
    df_alloc['% of Income'] = (df_alloc['Amount (£)'] / income * 100).round(1)

    st.subheader("📋 Recommended Allocation:")
    st.dataframe(df_alloc)

    # Pie chart
    st.subheader("📌 Visual Breakdown:")
    fig, ax = plt.subplots()
    ax.pie(df_alloc['Amount (£)'], labels=df_alloc.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("🔎 Rent & Food Expense Check")
    rent_flag = "✅ Within safe limit" if rent_input <= rent_max else "⚠️ Above recommended max"
    food_flag = "✅ Within safe limit" if food_input <= food_max else "⚠️ Above recommended max"

    st.markdown(f"**🏠 Your Rent:** £{rent_input} ({rent_flag}) — Recommended Max: £{rent_max}")
    st.markdown(f"**🍔 Your Food + Takeaways:** £{food_input} ({food_flag}) — Recommended Max: £{food_max}")

    st.markdown("""
    ✅ This plan is based on data from the ONS, UK student surveys, and job market insights.

    💡 Adjust the income or switch profiles to explore different financial scenarios.
    """)
