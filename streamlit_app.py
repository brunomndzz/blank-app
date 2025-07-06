import streamlit as st
import random

st.set_page_config(layout="wide")

# ── 1) Define a single scenario, with “correct” sign & value per line ─────────
transactions = [
    {
        "transaction": "Increase depreciation expense by $10 (40% tax)",
        "answers": {
            # Income Statement
            "Minus Dep&Amort":                        ("+", 10.0),
            "EBIT":                                   ("-", 10.0),
            "Pre-Tax Income":                         ("-", 10.0),
            "Minus Taxes (40%)":                      ("-",  4.0),
            "Net Income":                             ("-",  6.0),
            # Balance Sheet
            "PPE":                                    ("-", 10.0),
            "Accumulated Depreciation":               ("+", 10.0),
            "Retained Earnings":                      ("-",  6.0),
            # Cash Flow Statement
            "Depreciation & Amortization":            ("+", 10.0),
            "Cash flow from operating activities":    ("+",  4.0),
            "Ending cash balance":                    ("+",  4.0),
        },
    },
    {
        "transaction": "Revenue increases by $100 and OPEX increases by $40 (40% tax)",
        "answers": {
            # Income Statement
            "Revenue":                                ("+", 100.0),
            "Gross profit":                           ("+", 100.0),
            "OPEX":                                   ("+",  40.0),
            "EBIT":                                   ("+",  60.0),
            "Pre-Tax Income":                         ("+",  60.0),
            "Minus Taxes (40%)":                      ("-",  24.0),
            "Net Income":                             ("+",  36.0),
            # Balance Sheet
            "Cash":                                   ("+",  36.0),
            "Retained Earnings":                      ("+",  36.0),
            # Cash Flow Statement
            "Cash flow from operating activities":    ("+",  36.0),
            "Ending cash balance":                    ("+",  36.0),
        },
    },
    {
        "transaction": "Accounts Receivable increase of $50 (40% tax)",
        "answers": {
            # Income Statement
            "Revenue":                                ("+",  50.0),
            "Pre-Tax Income":                         ("+",  50.0),
            "Minus Taxes (40%)":                      ("-",  20.0),
            "Net Income":                             ("+",  30.0),
            # Balance Sheet
            "Accounts receivable":                    ("+",  50.0),
            "Cash":                                   ("-",  20.0),
            "Retained Earnings":                      ("+",  30.0),
            # Cash Flow Statement
            "Changes in Accounts receivable":         ("-",  50.0),
            "Cash flow from operating activities":    ("-",  20.0),
            "Ending cash balance":                    ("-",  20.0),
        },
    },
    {
        "transaction": "Depreciation increases by $30 (40% tax)",
        "answers": {
            # Income Statement
            "Minus Dep&Amort":                        ("+",  30.0),
            "EBIT":                                   ("-",  30.0),
            "Pre-Tax Income":                         ("-",  30.0),
            "Minus Taxes (40%)":                      ("-",  12.0),
            "Net Income":                             ("-",  18.0),
            # Balance Sheet
            "PPE":                                    ("-",  30.0),
            "Accumulated Depreciation":               ("+",  30.0),
            "Retained Earnings":                      ("-",  18.0),
            "Cash":                                   ("+",  12.0),
            # Cash Flow Statement
            "Depreciation & Amortization":            ("+",  30.0),
            "Cash flow from operating activities":    ("+",  12.0),
            "Ending cash balance":                    ("+",  12.0),
        },
    },
    {
        "transaction": "Purchase of PPE increases by $100",
        "answers": {
            # Cash Flow Statement
            "Purchase of PPE (CAPEX)":                ("-", 100.0),
            "Cash flow from investing activities":    ("-", 100.0),
            "Ending cash balance":                    ("-", 100.0),
            # Balance Sheet
            "Cash":                                   ("-", 100.0),
            "PPE":                                    ("+", 100.0),
        },
    },
    {
        "transaction": "Accounts payable increases by $70",
        "answers": {
            # Cash Flow Statement
            "Changes in Accounts payable":            ("+",  70.0),
            "Cash flow from operating activities":    ("+",  70.0),
            "Ending cash balance":                    ("+",  70.0),
            # Balance Sheet
            "Cash":                                   ("+",  70.0),
            "Accounts payable":                       ("+",  70.0),
        },
    },
    {
        "transaction": "New debt issuance of $150",
        "answers": {
            # Cash Flow Statement
            "Cash flow from financing activities":    ("+", 150.0),
            "Ending cash balance":                    ("+", 150.0),
            # Balance Sheet
            "Cash":                                   ("+", 150.0),
            "Term debt":                              ("+", 150.0),
        },
    },
    {
        "transaction": "Inventory increases by $60",
        "answers": {
            # Balance Sheet
            "Inventories":                            ("+",  60.0),
            "Cash":                                   ("-",  60.0),
            # Cash Flow Statement
            "Changes in Inventories":                 ("-",  60.0),
            "Cash flow from operating activities":    ("-",  60.0),
            "Ending cash balance":                    ("-",  60.0),
        },
    },
    {
        "transaction": "Deferred revenue decreases by $80 (40% tax)",
        "answers": {
            # Income Statement
            "Revenue":                                ("+",  80.0),
            "Pre-Tax Income":                         ("+",  80.0),
            "Minus Taxes (40%)":                      ("-",  32.0),
            "Net Income":                             ("+",  48.0),
            # Balance Sheet
            "Deferred revenue":                       ("-",  80.0),
            "Cash":                                   ("-",  32.0),
            "Retained Earnings":                      ("+",  48.0),
            # Cash Flow Statement
            "Changes in Deferred revenue":            ("-",  80.0),
            "Cash flow from operating activities":    ("-",  32.0),
            "Ending cash balance":                    ("-",  32.0),
        },
    },
    {
        "transaction": "Issuance of common stock by $100",
        "answers": {
            # Cash Flow Statement
            "Cash flow from financing activities":    ("+", 100.0),
            "Ending cash balance":                    ("+", 100.0),
            # Balance Sheet
            "Cash":                                   ("+", 100.0),
            "Common stock":                           ("+", 100.0),
        },
    },
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

# ── 5) Feedback ───────────────────────────────────────────────────────────────
if st.button("✅ Check Answers"):
    st.subheader("🧠 Feedback")

    def check_line(statement_name, line):
        sel_sign, sel_amt = st.session_state[f"{statement_name}_{line}"]
        corr_sign, corr_amt = answers.get(line, ("0", 0.0))
        ok = (sel_sign == corr_sign) and abs(sel_amt - corr_amt) < 1e-6
        color = "#D5F5E3" if ok else "#FADBD8"
        icon  = "✅" if ok else f"❌ (expected {corr_sign}{corr_amt})"
        st.markdown(
            f'<div style="background:{color};padding:4px;border-radius:3px">'
            f"{line}: {icon}</div>",
            unsafe_allow_html=True
        )

    st.markdown("**Income Statement**")
    for ln in income_lines:
        check_line("Income Statement", ln)

    st.markdown("**Balance Sheet**")
    for ln in bs_lines:
        check_line("Balance Sheet", ln)

    st.markdown("**Cash Flow Statement**")
    for ln in cfs_lines:
        check_line("Cash Flow Statement", ln)