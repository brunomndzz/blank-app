import streamlit as st
import random

st.set_page_config(layout="wide")

# ── 1) Define a single scenario, with “correct” sign & value per line ─────────
transactions = [
    {
        "transaction": "Increase depreciation expense by $10 (40% tax)",
        "answers": {
            # Income Statement
            "Minus Dep&Amort": ("+", 10.0),
            "EBIT": ("-", 10.0),
            "Pre-Tax Income": ("-", 10.0),
            "Minus Taxes (40%)": ("-", 4.0),
            "Net Income": ("-", 6.0),
            # Balance Sheet
            "PPE": ("-", 10.0),
            "Accumulated Depreciation": ("+", 10.0),
            "Retained Earnings": ("-", 6.0),
            # Cash Flow
            "Depreciation & Amortization": ("+", 10.0),
            "Cash flow from operating activities": ("+", 4.0),
            "Ending cash balance": ("+", 4.0),
        }
    },
    # … add more scenarios here
]

# ── 2) Define your row-labels for each statement ───────────────────────────────
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
    "Total Equity", "Total Liabilities & Equity"
]
cfs_lines = [
    "Net Income", "Depreciation & Amortization",
    "Changes in Accounts receivable", "Changes in Inventories",
    "Changes in Accounts payable", "Changes in Deferred revenue",
    "Cash flow from operating activities",
    "Purchase of PPE (CAPEX)", "Cash flow from investing activities",
    "Repayment of term debt Inc/dec Equity",
    "Proceeds from share issuance Inc/dec debt", "Dividends",
    "Cash flow from financing activities",
    "Beginning cash balance", "Total change in cash", "Ending cash balance"
]

sign_options = ["+", "-", "0"]  # 0 = no effect

# ── 3) Pick a random transaction ────────────────────────────────────────────────
if "tx" not in st.session_state:
    st.session_state.tx = random.choice(transactions)
if st.button("🔄 New Transaction"):
    st.session_state.tx = random.choice(transactions)

st.title("📊 3-Statement Line-Item Trainer")
st.write("**Scenario:**", st.session_state.tx["transaction"])
answers = st.session_state.tx["answers"]

# ── 4) Build three colored panels side by side ────────────────────────────────
col_is, col_bs, col_cfs = st.columns(3)

def render_statement(col, heading, lines, answer_dict):
    # Heading with dark background
    col.markdown(
        f'<div style="background:#2C3E50;color:white;padding:8px;border-radius:4px">'
        f'<strong>{heading}</strong></div>',
        unsafe_allow_html=True
    )
    # For each line create a 3-column row: label | sign | amount
    for line in lines:
        a_sign, a_val = answer_dict.get(line, ("0", 0.0))
        c1, c2, c3 = col.columns([3,1,1])
        c1.markdown(f"**{line}**")
        sel_sign = c2.selectbox("", sign_options, key=f"{heading}_{line}_sign")
        sel_amt  = c3.number_input("", min_value=0.0, format="%.2f",
                                   key=f"{heading}_{line}_amt")
        # store back into state for checking
        st.session_state[f"{heading}_{line}"] = (sel_sign, sel_amt)

# Income Statement
render_statement(col_is, "Income Statement", income_lines, answers)
# Balance Sheet
render_statement(col_bs, "Balance Sheet", bs_lines, answers)
# Cash Flow Statement
render_statement(col_cfs, "Cash Flow Statement", cfs_lines, answers)

# ── 5) Check Answers and show colored feedback ────────────────────────────────
if st.button("✅ Check Answers"):
    st.subheader("🧠 Feedback")
    def fb(line):
        sel_sign, sel_amt = st.session_state[f"{heading}_{line}"] \
            if heading == current_heading else (None,None)
        corr_sign, corr_amt = answers.get(line, ("0",0.0))
        ok = (sel_sign == corr_sign) and abs(sel_amt - corr_amt) < 0.01
        color = "#D5F5E3" if ok else "#FADBD8"
        return f'<div style="background:{color};padding:4px;border-radius:3px">' \
               f"{line}: {'✅' if ok else f'❌ (expected {corr_sign}{corr_amt})'}" \
               f'</div>'

    # Income feedback
    st.markdown("**Income Statement**")
    for line in income_lines:
        st.markdown(fb(line), unsafe_allow_html=True)

    # Balance feedback
    st.markdown("**Balance Sheet**")
    for line in bs_lines:
        st.markdown(fb(line), unsafe_allow_html=True)

    # CashFlow feedback
    st.markdown("**Cash Flow Statement**")
    for line in cfs_lines:
        st.markdown(fb(line), unsafe_allow_html=True)