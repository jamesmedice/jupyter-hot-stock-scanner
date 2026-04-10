import plotly.express as px
import os
from config import OUTPUT_DIR

def generate_correlation(df):
    metrics = [
        "HotScore", "MomentumScore", "VolumeScore",
        "VolumeSpike", "VolatilityScore", "TrendScore"
    ]

    corr = df[metrics].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Correlation Heatmap"
    )

    path = os.path.join(OUTPUT_DIR, "corr.html")
    fig.write_html(path)
    return path