import streamlit as st
import random

# 🔄 Transaction scenarios
transactions = [
    {
        "transaction": "Increase depreciation by $10",
        "IS": "Net income decreases",
        "BS": "PPE decreases, Retained Earnings decrease",
        "CFS": "CFO increases"
    },
    {
        "transaction": "Purchase equipment for $15 (CapEx)",
        "IS": "No effect",
        "BS": "PPE increases, Cash decreases",
        "CFS": "CFI decreases"
    },
    {
        "transaction": "Inventory increases by $10",
        "IS": "No effect",
        "BS": "Inventory increases, Cash decreases",
        "CFS": "CFO decreases"
    },
    {
        "transaction": "Accounts payable increases by $20",
        "IS": "No effect",
        "BS": "Liabilities increase, Cash increases",
        "CFS": "CFO increases"
    },
    {
        "transaction": "Issue $50 in equity",
        "IS": "No effect",
        "BS": "Cash increases, Equity increases",
        "CFS": "CFF increases"
    }
]

# 🔽 Dropdown answer choices
is_options = [
    "Net income decreases",
    "Net income increases",
    "No effect"
]

bs_options = [
    "PPE increases, Cash decreases",
    "PPE decreases, Retained Earnings decrease",
    "Inventory increases, Cash decreases",
    "Liabilities increase, Cash increases",
    "Cash increases, Equity increases",
    "Retained Earnings decrease",
    "No effect"
]

cfs_options = [
    "CFO increases",
    "CFO decreases",
    "CFI decreases",
    "CFF increases",
    "No effect"
]

# 🎯 App title
st.title("📊 3-Statement Transaction Trainer")

if "current" not in st.session_state:
    st.session_state.current = random.choice(transactions)

if st.button("🔄 New Transaction"):
    st.session_state.current = random.choice(transactions)

transaction = st.session_state.current
st.subheader("📦 Transaction")
st.write(transaction["transaction"])

# 🔽 Dropdown menus instead of text inputs
st.subheader("✍️ Your Answer (Choose from dropdowns)")
user_is = st.selectbox("Income Statement effect:", is_options)
user_bs = st.selectbox("Balance Sheet effect:", bs_options)
user_cfs = st.selectbox("Cash Flow Statement effect:", cfs_options)

# ✅ Check button and feedback
if st.button("✅ Check Answer"):
    st.subheader("🧠 Feedback")

    def check(user_input, correct):
        return "✅ Correct" if user_input == correct else f"❌ Expected: {correct}"

    st.markdown(f"**Income Statement:** {check(user_is, transaction['IS'])}")
    st.markdown(f"**Balance Sheet:** {check(user_bs, transaction['BS'])}")
    st.markdown(f"**Cash Flow Statement:** {check(user_cfs, transaction['CFS'])}")