import streamlit as st
import plotly.express as px
import pandas as pd

def render_stock_tab():

    df = pd.read_csv("../data/kmeans/interesting_stocks.csv")

    # Compute trade score
    df["trade_score"] = (
        0.35 * df["HotScore"] +
        0.25 * df["MomentumScore"] +
        0.20 * df["VolumeScore"] +
        0.15 * df["TrendScore"] +
        0.05 * df["VolatilityScore"]
    )

    st.subheader("High-Conviction Stock Signals")

    # Filters
    min_trade_score = st.slider(
        "Min Trade Score",
        float(df["trade_score"].min()),
        float(df["trade_score"].max()),
        0.85,
        step=0.01
    )

    min_volume_spike = st.slider(
        "Min Volume Spike",
        float(df["VolumeSpike"].min()),
        float(df["VolumeSpike"].max()),
        2.5,
        step=0.1
    )

    top_n = st.slider("Top N Stocks", 5, 50, 20)

    # Filter & aggregate
    filtered = df[
        (df["trade_score"] >= min_trade_score) &
        (df["VolumeSpike"] >= min_volume_spike)
    ]

    filtered = (
        filtered
        .groupby("symbol", as_index=False)
        .agg({
            "trade_score": "max",
            "HotScore": "mean",
            "MomentumScore": "mean",
            "TrendScore": "mean",
            "VolumeSpike": "max"
        })
        .sort_values("trade_score", ascending=False)
        .head(top_n)
    )

    # ------------------------
    # Horizontal bar chart: continuous color
    # ------------------------
    fig = px.bar(
        filtered.sort_values("trade_score"),
        x="trade_score",
        y="symbol",
        orientation="h",
        color="trade_score",  # continuous
        color_continuous_scale="Blues", 
        hover_data=["HotScore", "MomentumScore", "TrendScore", "VolumeSpike"],
        template="plotly_dark",
        text="trade_score"
    )

    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    fig.update_layout(
        paper_bgcolor="rgb(10,10,30)",
        plot_bgcolor="rgb(10,10,30)",
        xaxis=dict(title="Trade Score", color="white", range=[0, 1]),
        yaxis=dict(title="Symbol", color="white"),
        coloraxis_colorbar=dict(title="Trade Score"),
        height=600 + top_n*20,
        margin=dict(l=120, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered)
