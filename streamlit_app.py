import streamlit as st
import random

# 🔄 1) Define your transactions and, for each, the “correct” effect per line
transactions = [
    {
        "transaction": "Increase depreciation expense by $10 (40% tax rate)",
        "answers": {
            # Income Statement
            "Revenue":                   "No effect",
            "Minus COGS":                "No effect",
            "Gross profit":              "No effect",
            "OPEX":                      "No effect",
            "Minus SG&A":                "No effect",
            "Minus S&M":                 "No effect",
            "Minus R&D":                 "No effect",
            "Minus Dep&Amort":           "Increase",
            "EBIT":                      "Decrease",
            "Interest income or expense":"No effect",
            "Pre-Tax Income":            "Decrease",
            "Minus Taxes (40%)":         "Decrease",
            "Net Income":                "Decrease",
            # Balance Sheet
            "Cash":                      "No effect",
            "Accounts receivable":       "No effect",
            "Inventories":               "No effect",
            "Total current assets":      "No effect",
            "PPE":                       "No effect",
            "Accumulated Depreciation":  "Increase",
            "Net PPE":                   "Decrease",
            "Total non-current assets":  "No effect",
            "Total Assets":              "No effect",
            "Accounts payable":          "No effect",
            "Notes payable":             "No effect",
            "Deferred revenue":          "No effect",
            "Total current liabilities": "No effect",
            "Term debt":                 "No effect",
            "Total non-current liabilities":"No effect",
            "Total Liabilities":         "No effect",
            "Common stock":              "No effect",
            "Retained Earnings":         "Decrease",
            "Total Shareholders' Equity":"No effect",
            "Total Liabilities & Shareholders' Equity":"No effect",
            # Cash Flow Statement
            "Net Income":                "No effect",  # Net Income already flows in, but we won’t quiz here
            "Depreciation & Amortization":"Increase",
            "Changes in Accounts receivable":"No effect",
            "Changes in Inventories":"No effect",
            "Changes in Accounts payable":"No effect",
            "Changes in Notes payable":"No effect",
            "Changes in Deferred revenue":"No effect",
            "Cash flow from operating activities":"Increase",
            "Purchase of PPE (CAPEX)":"No effect",
            "Cash flow from investing activities":"No effect",
            "Repayment of term debt Inc/dec Equity":"No effect",
            "Proceeds from share issuance Inc/dec debt":"No effect",
            "Dividends":"No effect",
            "Cash flow from financing activities":"No effect",
            "Beginning cash balance":"No effect",
            "Total change in cash":"Increase",
            "Ending cash balance":"Increase",
        }
    },
    # … add your other transactions here
]

# 🔽 2) List out every row label exactly as in your sheet
income_lines = [
    "Revenue", "Minus COGS", "Gross profit",
    "OPEX", "Minus SG&A", "Minus S&M", "Minus R&D",
    "Minus Dep&Amort", "EBIT", "Interest income or expense",
    "Pre-Tax Income", "Minus Taxes (40%)", "Net Income"
]

bs_lines = [
    "Cash", "Accounts receivable", "Inventories", "Total current assets",
    "PPE", "Accumulated Depreciation", "Net PPE", "Total non-current assets",
    "Total Assets", "Accounts payable", "Notes payable", "Deferred revenue",
    "Total current liabilities", "Term debt", "Total non-current liabilities",
    "Total Liabilities", "Common stock", "Retained Earnings",
    "Total Shareholders' Equity", "Total Liabilities & Shareholders' Equity"
]

cfs_lines = [
    "Net Income", "Depreciation & Amortization",
    "Changes in Accounts receivable", "Changes in Inventories",
    "Changes in Accounts payable", "Changes in Notes payable",
    "Changes in Deferred revenue", "Cash flow from operating activities",
    "Purchase of PPE (CAPEX)", "Cash flow from investing activities",
    "Repayment of term debt Inc/dec Equity",
    "Proceeds from share issuance Inc/dec debt", "Dividends",
    "Cash flow from financing activities", "Beginning cash balance",
    "Total change in cash", "Ending cash balance"
]

# 3️⃣ The three choice options
options = ["Increase", "Decrease", "No effect"]

st.title("📊 3-Statement Line-Item Trainer")

# 4️⃣ Randomize which scenario you’re on
if "tx" not in st.session_state:
    st.session_state.tx = random.choice(transactions)
if st.button("🔄 New Transaction"):
    st.session_state.tx = random.choice(transactions)

st.subheader("📦 Transaction")
st.write(st.session_state.tx["transaction"])

# 5️⃣ Render the three columns of dropdowns
col1, col2, col3 = st.columns(3)

col1.header("Income Statement")
user_income = {
    line: col1.selectbox(line, options, key=f"is_{line}")
    for line in income_lines
}

col2.header("Balance Sheet")
user_bs = {
    line: col2.selectbox(line, options, key=f"bs_{line}")
    for line in bs_lines
}

col3.header("Cash Flow Statement")
user_cfs = {
    line: col3.selectbox(line, options, key=f"cfs_{line}")
    for line in cfs_lines
}

# 6️⃣ Check answers and show ✔️/❌
if st.button("✅ Check Answers"):
    st.subheader("🧠 Feedback")
    answers = st.session_state.tx["answers"]

    def feedback(line, selection):
        correct = answers.get(line, "No effect")
        return "✅" if selection == correct else f"❌ (expected {correct})"

    st.markdown("**Income Statement**")
    for line in income_lines:
        st.write(f"- {line}: {feedback(line, user_income[line])}")

    st.markdown("**Balance Sheet**")
    for line in bs_lines:
        st.write(f"- {line}: {feedback(line, user_bs[line])}")
col3.header("Cash Flow Statement")
user_cfs = {}
for line in cfs_lines:
    user_cfs[line] = col3.selectbox(line, options, key=f"cfs_{line}")
    