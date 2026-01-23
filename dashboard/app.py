import streamlit as st
import plotly.express as px
import pandas as pd


st.header("HOT STOCK MARKET", divider="rainbow")
st.set_page_config(layout="wide")

df = pd.read_csv("../data/kmeans/interesting_stocks.csv")

st.title("📈 Stock Signal Dashboard")

signal = st.selectbox("Signal", ["STRONG BUY", "WATCH", "IGNORE"])
confidence = st.slider("Min confidence", 0.5, 1.0, 0.8)

filtered = df[
    (df["predicted_signal"] == signal) &
    (df["confidence"] >= confidence)
]

fig = px.scatter(
    filtered,
    x="HotScore",
    y="VolumeSpike",
    color="confidence",
    hover_data=["symbol"],
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
st.dataframe(filtered)
