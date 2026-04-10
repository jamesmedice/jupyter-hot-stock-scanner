from charts.bar import generate_bar_chart
from charts.heatmap import generate_heatmap
from charts.correlation import generate_correlation

def chart_agent(state):
    df = state["filtered_df"]
    chart_type = state["chart_type"]

    if df.empty:
        return {"chart_path": None}

    if chart_type == "heatmap":
        path = generate_heatmap(df)
    elif chart_type == "correlation":
        path = generate_correlation(df)
    else:
        path = generate_bar_chart(df)

    return {"chart_path": path}