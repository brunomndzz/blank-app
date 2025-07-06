import streamlit as st
import pandas as pd
import random

# ── Setup ─────────────────────────────────────────────────────────────────────
st.set_page_config(layout="wide")
sign_options = ["+", "-", "0"]  # 0 = no effect

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

# ── 2) Line labels ─────────────────────────────────────────────────────────────
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
    "Cash flow from financing activities", "Ending cash balance"
]

# ── 3) Helper to build a zeroed DataFrame and apply the answers ───────────────
def build_df(lines, changes):
    df = pd.DataFrame(0.0, index=lines, columns=["Change"])
    for line, val in changes.items():
        if line in df.index:
            # val might be ("+", amount) or already a number
            amt = val[1] if (isinstance(val, tuple) and len(val) >= 2) else val
            df.at[line, "Change"] = amt
    return df.round(2)

# ── 4) Styling functions ──────────────────────────────────────────────────────
def style_income(df: pd.DataFrame):
    return (
        df.style
          .set_caption("<b>Income Statement Changes</b>")
          .format("{:+.2f}")
          .set_table_styles([
              {"selector": "thead", "props": [("background-color", "#f9e79f")]},
              {"selector": "tbody tr", "props": [("background-color", "#fcf3cf")]}
          ])
          .set_properties(**{"text-align": "right"})
    )

def style_balance(df: pd.DataFrame):
    def section_color(row):
        if row.name in bs_lines[:9]:
            color = "#ee1d0a"
        elif row.name in bs_lines[9:16]:
            color = "#ee1d0a"
        else:
            color = "#ee1d0a"
        return [f"background-color: {color};"] * len(row)

    return (
        df.style
          .set_caption("<b>Balance Sheet Changes</b>")
          .format("{:+.2f}")
          .apply(section_color, axis=1)
          .set_properties(**{"text-align": "right"})
    )

def style_cashflow(df: pd.DataFrame):
    def cf_color(row):
        key = row.name.lower()
        if "operating" in key:
            color = "#013a19"
        elif "investing" in key:
            color = "#013a19"
        else:
            color = "#013a19"
        return [f"background-color: {color};"] * len(row)

    return (
        df.style
          .set_caption("<b>Cash Flow Statement Changes</b>")
          .format("{:+.2f}")
          .apply(cf_color, axis=1)
          .set_properties(**{"text-align": "right"})
    )

# ── 5) Pick & display the scenario inputs ─────────────────────────────────────
if "tx" not in st.session_state:
    st.session_state.tx = random.choice(transactions)
if st.button("🔄 New Transaction"):
    st.session_state.tx = random.choice(transactions)

st.title("📊 3-Statement Transaction Trainer")
st.markdown(f"**Scenario:** {st.session_state.tx['transaction']}")
answers = st.session_state.tx["answers"]

# ── 6) Render the interactive dropdowns & number inputs ──────────────────────
col_is, col_bs, col_cfs = st.columns(3)

def render_statement(col, heading, lines):
    col.markdown(
        f'<div style="background:#2C3E50;color:white;padding:8px;border-radius:4px">'
        f'<strong>{heading}</strong></div>',
        unsafe_allow_html=True
    )
    for line in lines:
        c1, c2, c3 = col.columns([3, 1, 1])
        c1.markdown(f"**{line}**")
        sel_sign = c2.selectbox("", sign_options, key=f"{heading}_{line}_sign")
        sel_amt  = c3.number_input("", min_value=0.0, format="%.2f",
                                  key=f"{heading}_{line}_amt")
        st.session_state[f"{heading}_{line}"] = (sel_sign, sel_amt)

render_statement(col_is, "Income Statement", income_lines)
render_statement(col_bs, "Balance Sheet", bs_lines)
render_statement(col_cfs, "Cash Flow Statement", cfs_lines)

# ── 7) Show styled simulation of the “correct” answers ───────────────────────
if st.button("📝 Show Statement Changes"):
    is_df  = build_df(income_lines, answers)
    bs_df  = build_df(bs_lines,     answers)
    cfs_df = build_df(cfs_lines,    answers)

    tab1, tab2, tab3 = st.tabs([
        "Income Statement", "Balance Sheet", "Cash Flow Statement"
    ])
    with tab1:
        st.write(style_income(is_df))
    with tab2:
        st.write(style_balance(bs_df))
    with tab3:
        st.write(style_cashflow(cfs_df))
# ── 8) Check the user’s inputs and give feedback ─────────────────────────────
if st.button("✅ Check Answers"):
    with st.expander("🧠 Feedback", expanded=True):
        def check_line(statement, line):
            sel_sign, sel_amt = st.session_state[f"{statement}_{line}"]
            corr_sign, corr_amt = answers.get(line, ("0", 0.0))
            ok    = (sel_sign == corr_sign) and abs(sel_amt - corr_amt) < 1e-6
            color = "#000000" if ok else "#07079C"
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
