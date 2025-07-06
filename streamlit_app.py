if st.button("✅ Check Answers"):
    st.subheader("🧠 Feedback")
    def check_line(statement_name, line):
        # pull your selected sign & amount from session_state
        sel_sign, sel_amt = st.session_state[f"{statement_name}_{line}"]
        # pull the correct answer from your transaction dict
        corr_sign, corr_amt = answers.get(line, ("0", 0.0))
        # compare
        ok = (sel_sign == corr_sign) and abs(sel_amt - corr_amt) < 1e-6
        # color & icon
        color = "#D5F5E3" if ok else "#FADBD8"
        icon  = "✅" if ok else f"❌ (expected {corr_sign}{corr_amt})"
        # render a colored div
        st.markdown(
            f'<div style="background:{color};padding:4px;border-radius:3px">'
            f"{line}: {icon}</div>",
            unsafe_allow_html=True
        )

    # Income Statement feedback
    st.markdown("**Income Statement**")
    for line in income_lines:
        check_line("Income Statement", line)

    # Balance Sheet feedback
    st.markdown("**Balance Sheet**")
    for line in bs_lines:
        check_line("Balance Sheet", line)

    # Cash Flow feedback
    st.markdown("**Cash Flow Statement**")
    for line in cfs_lines:
        check_line("Cash Flow Statement", line)