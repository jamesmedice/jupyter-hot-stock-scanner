import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Hot Stocks Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("HOT STOCK MARKET", divider="gray")  

confidence_tab = st.tabs(["Stock's Filter"])[0]

from interesting_stock  import render_stock_tab

with confidence_tab:
    render_stock_tab()

