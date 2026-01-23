import streamlit as st
import plotly.express as px
import pandas as pd
 

def render_stock_tab ():

    df = pd.read_csv("../data/kmeans/interesting_stocks.csv")

    df["trade_score"] = (
            0.35 * df["HotScore"] +
            0.25 * df["MomentumScore"] +
            0.20 * df["VolumeScore"] +
            0.15 * df["TrendScore"] +
            0.05 * df["VolatilityScore"]
        )

    st.subheader("High-Conviction Stock Signals")

    df["trade_score"] = (
        0.35 * df["HotScore"] +
        0.25 * df["MomentumScore"] +
        0.20 * df["VolumeScore"] +
        0.15 * df["TrendScore"] +
        0.05 * df["VolatilityScore"]
    )

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

    fig = px.scatter(
        filtered,
        x="HotScore",
        y="VolumeSpike",
        color="symbol", 
        hover_data=["symbol"],
        template="plotly_dark",    
    )

    fig.update_layout(      
        paper_bgcolor="#272727",   
        plot_bgcolor="#0B8600",    
        xaxis=dict(title="HotScore", color="white"),
        yaxis=dict(title="VolumeSpike", color="white"),
        legend=dict(title="symbol", font=dict(color="white"))
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered)