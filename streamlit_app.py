import streamlit as st
import random

# Define sample transactions and effects
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
        "transaction": "Accounts Payable increases by $20",
        "IS": "No effect",
        "BS": "Liabilities increase, Cash increases",
        "CFS": "CFO increases"
    },
    {
        "transaction": "Inventory increases by $10",
        "IS": "No effect",
        "BS": "Inventory increases, Cash decreases",
        "CFS": "CFO decreases"
    },
    {
        "transaction": "Issue $50 in equity",
        "IS": "No effect",
        "BS": "Cash increases, Equity increases",
        "CFS": "CFF increases"
    },
]

st.title("📊 3-Statement Transaction Trainer")

if "current" not in st.session_state:
    st.session_state.current = random.choice(transactions)

if st.button("🔄 New Transaction"):
    st.session_state.current = random.choice(transactions)

transaction = st.session_state.current
st.subheader("📦 Transaction")
st.write(transaction["transaction"])

# User inputs
st.subheader("✍️ Your Answer")
user_is = st.text_input("What happens to the **Income Statement**?")
user_bs = st.text_input("What happens to the **Balance Sheet**?")
user_cfs = st.text_input("What happens to the **Cash Flow Statement**?")

if st.button("✅ Check Answer"):
    st.subheader("🧠 Feedback")

    def check(user_input, correct):
        return "✅ Correct" if correct.lower() in user_input.lower() else f"❌ Expected: {correct}"

    st.markdown(f"**Income Statement:** {check(user_is, transaction['IS'])}")
    st.markdown(f"**Balance Sheet:** {check(user_bs, transaction['BS'])}")
    st.markdown(f"**Cash Flow Statement:** {check(user_cfs, transaction['CFS'])}")

