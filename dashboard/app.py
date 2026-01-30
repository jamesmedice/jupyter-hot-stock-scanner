import streamlit as st

st.set_page_config(
    page_title="Hot Stocks Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("HOT STOCK MARKET", divider="gray")  

confidence_tab, final_rank = st.tabs(["Hot Stock's Filter", "Final Rank Filter"])

from interesting_stock  import render_stock_tab as render_confidence_tab

with confidence_tab:
    render_confidence_tab()

from final_rank import render_stock_tab as render_final_rank_tab

with final_rank:
    render_final_rank_tab()