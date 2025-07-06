import streamlit as st
import random
import pandas as pd

st.set_page_config(layout="wide")

# ── 1) Define your transactions ───────────────────────────────────────────────
transactions = [
    {
        "transaction": "Inventory increases by $60",
        "answers": {
            # Income Statement (no impact)
            # Balance Sheet
            "Inventories":                          +60.0,
            "Cash":                                 -60.0,
            # Cash Flow
            "Changes in Inventories":               -60.0,
            "Cash flow from operating activities":  -60.0,
            "Ending cash balance":                  -60.0,
        },
    },
    # … add more scenarios here …
]

# ── 2) Define your row labels ─────────────────────────────────────────────────
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


# ── 3) Builders: create zeroed DataFrames + populate with answers ────────────
def build_df(lines, changes):
    df = pd.DataFrame(0.0, index=lines, columns=["Change"])
    for line, amt in changes.items():
        if line in df.index:
            df.at[line, "Change"] = amt
    return df.round(2)


# ── 4) Styler functions for each statement ────────────────────────────────────
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
    def section_color(idx):
        # first 9 = assets, next 7 = liabilities, rest = equity
        if idx in bs_lines[:9]:
            return ["#fadbd8"]  # light red
        if idx in bs_lines[9:16]:
            return ["#f5b7b1"]  # pink
        return ["#fadbd8"]
    return (
        df.style
          .set_caption("<b>Balance Sheet Changes</b>")
          .format("{:+.2f}")
          .apply(lambda row: section_color(row.name), axis=1)
          .set_properties(**{"text-align": "right"})
    )

def style_cashflow(df: pd.DataFrame):
    def cf_color(idx):
        if "operating" in idx.lower():
            return ["#d5f5e3"]  # light green
        if "investing" in idx.lower():
            return ["#a9dfbf"]
        return ["#d5f5e3"]
    return (
        df.style
          .set_caption("<b>Cash Flow Statement Changes</b>")
          .format("{:+.2f}")
          .apply(lambda row: cf_color(row.name), axis=1)
          .set_properties(**{"text-align": "right"})
    )


# ── 5) Main App ──────────────────────────────────────────────────────────────
st.title("📊 3-Statement Transaction Trainer")
scenario = st.selectbox(
    "Select a transaction:",
    [tx["transaction"] for tx in transactions]
)
tx = next(tx for tx in transactions if tx["transaction"] == scenario)
answers = tx["answers"]

# Use tabs to separate output cleanly
tab_is, tab_bs, tab_cfs = st.tabs([
    "Income Statement", "Balance Sheet", "Cash Flow Statement"
])

# Build DataFrames
is_df  = build_df(income_lines, answers)
bs_df  = build_df(bs_lines,     answers)
cfs_df = build_df(cfs_lines,    answers)

with tab_is:
    st.write(style_income(is_df))

with tab_bs:
    st.write(style_balance(bs_df))

with tab_cfs:
    st.write(style_cashflow(cfs_df))