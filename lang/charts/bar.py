import plotly.express as px
import os
from config import OUTPUT_DIR

def generate_bar_chart(df):
    df = df.copy()

    df["score_norm"] = (
        (df["HotScore"] - df["HotScore"].min()) /
        (df["HotScore"].max() - df["HotScore"].min() + 1e-9)
    )

    fig = px.bar(
        df.sort_values("HotScore"),
        x="HotScore",
        y="symbol",
        orientation="h",
        color="score_norm",
        title="AI Stock Bar Chart"
    )

    path = os.path.join(OUTPUT_DIR, "bar.html")
    fig.write_html(path)
    return path