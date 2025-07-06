import streamlit as st
import pandas as pd
import random

# ── SETUP & GLOBAL CSS ─────────────────────────────────────────────────────────
st.set_page_config(layout="wide")
st.markdown("""
    <style>
      /* Global font, dark background */
      html, body, [class*="css"] { 
        font-family: 'Segoe UI', sans-serif; 
        background: #1e1e1e; 
        color: #ddd;
      }
      .stApp { padding: 1.5rem; }

      /* Section headers */
      .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #fff;
        border-bottom: 2px solid #444;
        padding-bottom: 0.25rem;
        margin-bottom: 0.75rem;
      }

      /* Label vs control cells */
      .label-cell { text-align: left; }
      .control-cell { text-align: right; }

      /* Uniform input widths */
      .stSelectbox, .stNumberInput > div {
        width: 4.5rem !important;
        display: inline-block;
      }
    </style>
""", unsafe_allow_html=True)

sign_options = ["+", "-", "0"]  # 0 = no effect

# ── 1) Your Transactions ────────────────────────────────────────────────────────
transactions = [
    {
        "transaction": "Increase depreciation expense by $10 (40% tax)",
        "answers": {
            # Income Statement
            "Minus Dep&Amort":                     ("+", 10.0),
            "EBIT":                                  ("-", 10.0),
            "Pre-Tax Income":                        ("-", 10.0),
            "Minus Taxes (40%)":                     ("-",  4.0),
            "Net Income":                            ("-",  6.0),
            # Balance Sheet
            "PPE":                                   ("-", 10.0),
            "Accumulated Depreciation":             ("+", 10.0),
            "Retained Earnings":                    ("-",  6.0),
            # Cash Flow Statement
            "Depreciation & Amortization":           ("+", 10.0),
            "Cash flow from operating activities":   ("+",  4.0),
            "Ending cash balance":                   ("+",  4.0),
        },
    },
    {
        "transaction": "Revenue increases by $100 and OPEX increases by $40 (40% tax)",
        "answers": {
            # Income Statement
            "Revenue":                               ("+", 100.0),
            "Gross profit":                          ("+", 100.0),
            "OPEX":                                  ("+",  40.0),
            "EBIT":                                  ("+",  60.0),
            "Pre-Tax Income":                        ("+",  60.0),
            "Minus Taxes (40%)":                     ("-",  24.0),
            "Net Income":                            ("+",  36.0),
            # Balance Sheet
            "Cash":                                  ("+",  36.0),
            "Retained Earnings":                     ("+",  36.0),
            # Cash Flow Statement
            "Cash flow from operating activities":   ("+",  36.0),
            "Ending cash balance":                   ("+",  36.0),
        },
    },
    {
        "transaction": "Accounts Receivable increase of $50 (40% tax)",
        "answers": {
            # Income Statement
            "Revenue":                               ("+",  50.0),
            "Pre-Tax Income":                        ("+",  50.0),
            "Minus Taxes (40%)":                     ("-",  20.0),
            "Net Income":                            ("+",  30.0),
            # Balance Sheet
            "Accounts receivable":                   ("+",  50.0),
            "Cash":                                  ("-",  20.0),
            "Retained Earnings":                     ("+",  30.0),
            # Cash Flow Statement
            "Changes in Accounts receivable":        ("-",  50.0),
            "Cash flow from operating activities":   ("-",  20.0),
            "Ending cash balance":                   ("-",  20.0),
        },
    },
    # … add your other scenarios here …
]

# ── 2) Row-labels ────────────────────────────────────────────────────────────────
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

# ── 3) Build zeroed DataFrame & populate ───────────────────────────────────────
def build_df(lines, changes):
    df = pd.DataFrame(0.0, index=lines, columns=["Change"])
    for line, val in changes.items():
        if line in df.index:
            amt = val[1] if isinstance(val, tuple) else val
            df.at[line, "Change"] = amt
    return df.round(2)

# ── 4) Styling for each statement ──────────────────────────────────────────────
def style_income(df):
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

def style_balance(df):
    def color_row(r):
        if r.name in bs_lines[:9]:
            c = "#fadbd8"
        elif r.name in bs_lines[9:16]:
            c = "#f5b7b1"
        else:
            c = "#fadbd8"
        return [f"background-color: {c};"] * len(r)
    return (
        df.style
          .set_caption("<b>Balance Sheet Changes</b>")
          .format("{:+.2f}")
          .apply(color_row, axis=1)
          .set_properties(**{"text-align": "right"})
    )

def style_cashflow(df):
    def color_row(r):
        key = r.name.lower()
        if "operating" in key:
            c = "#d5f5e3"
        elif "investing" in key:
            c = "#a9dfbf"
        else:
            c = "#d5f5e3"
        return [f"background-color: {c};"] * len(r)
    return (
        df.style
          .set_caption("<b>Cash Flow Statement Changes</b>")
          .format("{:+.2f}")
          .apply(color_row, axis=1)
          .set_properties(**{"text-align": "right"})
    )

# ── 5) Pick & display scenario ─────────────────────────────────────────────────
if "tx" not in st.session_state:
    st.session_state.tx = random.choice(transactions)
if st.button("🔄 New Transaction"):
    st.session_state.tx = random.choice(transactions)

st.title("📊 3-Statement Transaction Trainer")
st.markdown(f"**Scenario:** {st.session_state.tx['transaction']}")
answers = st.session_state.tx["answers"]

# ── 6) Render inputs in a 3-column grid ────────────────────────────────────────
col_is, col_bs, col_cfs = st.columns(3)

def render_statement(col, heading, lines):
    col.markdown(f'<div class="section-header">{heading}</div>', unsafe_allow_html=True)
    for line in lines:
        lc, sc, nc = col.columns([4,1,1], gap="small")
        lc.markdown(f'<div class="label-cell">{line}</div>', unsafe_allow_html=True)
        sign = sc.selectbox("", sign_options, key=f"{heading}_{line}_sign", label_visibility="collapsed")
        amt  = nc.number_input("", min_value=0.0, format="%.2f",
                               key=f"{heading}_{line}_amt", label_visibility="collapsed")
        st.session_state[f"{heading}_{line}"] = (sign, amt)

render_statement(col_is, "Income Statement",     income_lines)
render_statement(col_bs, "Balance Sheet",         bs_lines)
render_statement(col_cfs,"Cash Flow Statement",   cfs_lines)

# ── 7) “Show Statement Changes” ───────────────────────────────────────────────
if st.button("📝 Show Statement Changes"):
    is_df  = build_df(income_lines, answers)
    bs_df  = build_df(bs_lines,     answers)
    cfs_df = build_df(cfs_lines,    answers)
    t1,t2,t3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow Statement"])
    with t1: st.write(style_income(is_df))
    with t2: st.write(style_balance(bs_df))
    with t3: st.write(style_cashflow(cfs_df))

# ── 8) Check user inputs & feedback ────────────────────────────────────────────
if st.button("✅ Check Answers"):
    with st.expander("🧠 Feedback", expanded=True):
        def check_line(stmt, line):
            sel_sign, sel_amt = st.session_state[f"{stmt}_{line}"]
            corr_sign, corr_amt = answers.get(line, ("0", 0.0))
            ok = sel_sign == corr_sign and abs(sel_amt - corr_amt) < 1e-6
            bg = "#2ecc71" if ok else "#e74c3c"
            ico = "✅" if ok else f"❌ (exp: {corr_sign}{corr_amt})"
            st.markdown(
                f'<div style="background:{bg};padding:4px;border-radius:3px">'
                f"{line}: {ico}</div>", unsafe_allow_html=True
            )

        st.markdown("**Income Statement**")
        for ln in income_lines:      check_line("Income Statement", ln)
        st.markdown("**Balance Sheet**")
        for ln in bs_lines:          check_line("Balance Sheet", ln)
        st.markdown("**Cash Flow Statement**")
        for ln in cfs_lines:         check_line("Cash Flow Statement", ln)