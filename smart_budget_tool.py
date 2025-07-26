import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

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
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eef2f3 0%, #cfd9df 100%);
        font-family: 'Segoe UI', sans-serif;
        color: #1a1a1a;
    }
    h1 {
        font-family: 'Poppins', sans-serif;
        color: #003366;
        font-size: 3.2em;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.3em;
    }
    .subtitle {
        font-size: 1.3em;
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    .guide-box {
        background-color: #e6f2ff;
        border-left: 5px solid #1a75ff;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 30px;
        font-size: 1.05em;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<h1>📊 Smart Budget Allocation Tool</h1>
<div class="subtitle">Your intelligent personal finance guide built with data, logic, and simplicity</div>
<div class="guide-box">
🚀 How to Use This App:<br>
👉 Use the left sidebar to enter your income, user profile, and monthly rent/food costs.<br>
📊 Then hit "Generate My Budget Plan" to see your personalised financial breakdown.<br>
🎯 You'll get insights, suggestions, and warnings where you're overspending.<br>
💡 Optimise your money decisions with confidence — powered by UK finance data.
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🛠 User Input")
income = st.sidebar.number_input("Enter your monthly income (£):", min_value=100, max_value=10000, value=1200)
profile = st.sidebar.selectbox("Select your profile:", ["Student", "Graduate", "Tier 2 Skilled Worker", "Other"])
rent_input = st.sidebar.number_input("Your current rent (£ per month):", min_value=0, max_value=5000, value=600)
groceries_input = st.sidebar.number_input("Groceries (£ per month):", min_value=0, max_value=2000, value=100)
takeaway_input = st.sidebar.number_input("Takeaways/Restaurants (£ per month):", min_value=0, max_value=2000, value=50)

# Calculate and Display Results
if st.sidebar.button("Generate My Budget Plan"):
    allocation, rent_max, food_max = get_allocation(income, profile)
    df_alloc = pd.DataFrame.from_dict(allocation, orient='index', columns=['Amount (£)'])
    df_alloc['% of Income'] = (df_alloc['Amount (£)'] / income * 100).round(1)

    st.subheader("📋 Recommended Monthly Allocation")
    st.dataframe(df_alloc.style.format({"Amount (£)": "£{:.2f}", "% of Income": "{:.1f}%"}))

    # Plotly Pie Chart
    fig = px.pie(df_alloc.reset_index(), names='index', values='Amount (£)',
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 title="Budget Breakdown by Category")
    st.plotly_chart(fig, use_container_width=True)

    # Rent & Food Spending Check
    st.subheader("🔎 Rent & Food Expense Check")
    food_input = groceries_input + takeaway_input
    rent_flag = "✅ Within safe limit" if rent_input <= rent_max else f"⚠️ Above recommended max by £{rent_input - rent_max:.2f}"
    food_flag = "✅ Within safe limit" if food_input <= food_max else f"⚠️ Above recommended max by £{food_input - food_max:.2f}"

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏠 Your Rent", f"£{rent_input}", help=f"Max recommended: £{rent_max}")
        st.markdown(rent_flag)
        if rent_input > rent_max:
            st.info(f"💡 Try reducing your rent cost by at least £{rent_input - rent_max:.2f} to meet the recommended limit.")
    with col2:
        st.metric("🍔 Total Food (Groceries + Takeaways)", f"£{food_input}", help=f"Max recommended: £{food_max}")
        st.markdown(food_flag)
        if food_input > food_max:
            st.info(f"💡 Consider cutting down your food-related expenses by £{food_input - food_max:.2f} to align with healthy budgeting.")

    style_metric_cards(background_color="#FFFFFF", border_left_color="#3399FF", border_color="#E0E0E0")

    st.markdown("""
    ✅ This plan is based on data from the ONS, UK student surveys, and job market insights.

    📈 Adjust your values to simulate different financial scenarios.
    """)
