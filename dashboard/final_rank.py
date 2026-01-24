import streamlit as st
import plotly.express as px
import pandas as pd

def render_stock_tab():
    df = pd.read_csv("../data/kmeans/rank_stocks.csv")

    # ------------------------
    # Compute trade_score
    # ------------------------
    df["trade_score"] = (
        0.35 * df["HotScore"] +
        0.25 * df["MomentumScore"] +
        0.20 * df["VolumeScore"] +
        0.15 * df["TrendScore"] +
        0.05 * df["VolatilityScore"]
    )

    st.subheader("High-Conviction Stock Signals")
    st.markdown("Filter the stocks by AI signals, KNN uniqueness, and final rank.")

    # ------------------------
    # Page filters (instead of sidebar)
    # ------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        final_signal_filter = st.multiselect(
            "Final Signal",
            options=df["final_signal"].unique(),
            default=df["final_signal"].unique()
        )

    with col2:
        knn_signal_filter = st.multiselect(
            "KNN Signal",
            options=df["knn_signal"].unique(),
            default=df["knn_signal"].unique()
        )

    with col3:
        min_rank = st.slider(
            "Minimum Final Rank",
            min_value=float(df["final_rank"].min()),
            max_value=float(df["final_rank"].max()),
            value=float(df["final_rank"].min())
        )

    # ------------------------
    # Apply filters
    # ------------------------
    filtered = df[
        (df["final_signal"].isin(final_signal_filter)) &
        (df["knn_signal"].isin(knn_signal_filter)) &
        (df["final_rank"] >= min_rank)
    ].copy()

    st.subheader(f"Filtered Stocks: {len(filtered)} rows")

    # ------------------------
    # Display table
    # ------------------------
    st.dataframe(filtered)

    # ------------------------
    # Heatmap of metrics
    # ------------------------
    metrics = ["HotScore", "MomentumScore", "VolumeScore", 
               "VolumeSpike", "VolatilityScore", "TrendScore", "knn_uniqueness"]

    df_heat = filtered.copy()
    for col in metrics:
        df_heat[col] = (df_heat[col] - df_heat[col].min()) / (df_heat[col].max() - df_heat[col].min())

    if not df_heat.empty:
        fig = px.imshow(
            df_heat[metrics].T,
            x=df_heat["symbol"],
            y=metrics,
            color_continuous_scale="Blues",
            text_auto=True,
            aspect="auto"
        )
        
        fig.update_layout(
            template="plotly_dark",
            title="Metrics Heatmap",
            xaxis=dict(title="Symbol", tickangle=-45, tickfont=dict(color="white")),
            yaxis=dict(title="Metric", tickfont=dict(color="white")),
            coloraxis_colorbar=dict(title="Normalized Value"),
            paper_bgcolor="rgb(10,10,30)",
            plot_bgcolor="rgb(10,10,30)",
            height=700,
            margin=dict(l=100, r=40, t=80, b=150)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No stocks match the current filter. Adjust the filters above.")
