import plotly.graph_objects as go
import os
from config import OUTPUT_DIR

def generate_heatmap(df):
    metrics = [
        "HotScore", "MomentumScore", "VolumeScore",
        "VolumeSpike", "VolatilityScore", "TrendScore"
    ]

    df = df.copy()

    for col in metrics:
        min_v = df[col].min()
        max_v = df[col].max()
        df[col] = (df[col] - min_v) / (max_v - min_v + 1e-9)

    z = df[metrics].values.T

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=df["symbol"],
        y=metrics,
        colorscale="Blues"
    ))

    path = os.path.join(OUTPUT_DIR, "heatmap.html")
    fig.write_html(path)
    return path