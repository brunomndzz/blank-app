import streamlit as st
import random

# Make the page use the full browser width
st.set_page_config(layout="wide")

# ── 1) Define scenarios with per-line correct sign & value ───────────────────
transactions = [
    {
        "transaction": "Increase depreciation expense by $10 (40% tax)",
        "answers": {
            # ─── Income Statement ─────────────────────────────
            "Minus Dep&Amort":    ("+", 10.0),   # depreciation ↑10
            "EBIT":               ("-", 10.0),   # EBIT ↓10
            "Pre-Tax Income":     ("-", 10.0),   # pre-tax ↓10
            "Minus Taxes (40%)":  ("-",  4.0),   # tax expense ↓4
            "Net Income":         ("-",  6.0),   # net income ↓6

            # ─── Balance Sheet ─────────────────────────────
            "Cash":                      ("+",  4.0),  # cash ↑4
            "PPE":                       ("-", 10.0),  # PPE ↓10
            "Accumulated Depreciation":  ("+", 10.0),  # Accum Depr ↑10
            "Retained Earnings":         ("-",  6.0),  # RE ↓6

            # ─── Cash Flow Statement ────────────────────────
            "Net Income":                     ("-",  6.0),  # starting NI ↓6
            "Depreciation & Amortization":    ("+", 10.0),  # add‐back +10
            "Changes in Accounts receivable": ("0",   0.0),
            "Changes in Inventories":         ("0",   0.0),
            "Changes in Accounts payable":    ("0",   0.0),
            "Changes in Deferred revenue":    ("0",   0.0),
            "Cash flow from operating activities": ("+",  4.0),  # net +4
            "Purchase of PPE (CAPEX)":            ("0",   0.0),
            "Cash flow from investing activities":("0",   0.0),
            "Repayment of term debt Inc/dec Equity":("0",0.0),
            "Proceeds from share issuance Inc/dec debt":("0",0.0),
            "Dividends":                          ("0",   0.0),
            "Cash flow from financing activities":("0",   0.0),
            "Beginning cash balance":             ("0",   0.0),
            "Total change in cash":               ("+",   4.0),
            "Ending cash balance":                ("+",   4.0),
        }
    },

    # … add more here …
]

# ── 2) Row labels exactly as in your template ─────────────────────────────────
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

# ── 3) Pick & display the scenario ────────────────────────────────────────────
if "tx" not in st.session_state:
    st.session_state.tx = random.choice(transactions)
if st.button("🔄 New Transaction"):
    st.session_state.tx = random.choice(transactions)

st.title("📊 3-Statement Line-Item Trainer")
st.markdown(f"**Scenario:** {st.session_state.tx['transaction']}")
answers = st.session_state.tx["answers"]

# ── 4) Render all three statements side by side ───────────────────────────────
col1, col2, col3 = st.columns(3)

def render(col, title, lines):
    col.markdown(
        f'<div style="background:#2C3E50;color:white;padding:8px;border-radius:4px">'
        f'<strong>{title}</strong></div>',
        unsafe_allow_html=True
    )
    for line in lines:
        corr_sign, corr_amt = answers.get(line, ("0", 0.0))
        c_label, c_sign, c_amt = col.columns([3, 1, 1])
        c_label.markdown(f"**{line}**")
        sel_sign = c_sign.selectbox("", sign_options, key=f"{title}_{line}_sign")
        sel_amt  = c_amt.number_input(
            "", min_value=0.0, format="%.2f", key=f"{title}_{line}_amt"
        )
        # store for feedback
        st.session_state[f"{title}_{line}"] = (sel_sign, sel_amt)

render(col1, "Income Statement", income_lines)
render(col2, "Balance Sheet", bs_lines)
render(col3, "Cash Flow Statement", cfs_lines)

# ── 5) Feedback ───────────────────────────────────────────────────────────────
if st.button("✅ Check Answers"):
    st.subheader("🧠 Feedback")

    def check_line(title, line):
        sel_sign, sel_amt = st.session_state[f"{title}_{line}"]
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
    for ln in income_lines: check_line("Income Statement", ln)

    st.markdown("**Balance Sheet**")
    for ln in bs_lines:      check_line("Balance Sheet", ln)

    st.markdown("**Cash Flow Statement**")
    for ln in cfs_lines:     check_line("Cash Flow Statement", ln)
    