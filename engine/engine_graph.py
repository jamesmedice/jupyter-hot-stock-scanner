# ============================================
# AI STOCK ANALYZER V2 (LangGraph Multi-Agent)
# ============================================

import os
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from typing import TypedDict, Dict, Any

#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

# ============================================
# CONFIG
# ============================================
DATA_PATH = "ml/features_base.csv"
OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# LOAD DATA
# ============================================
df = pd.read_csv(DATA_PATH)

# ============================================
# LLM
# ============================================
token = os.environ["GITHUB_TOKEN"]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=token,
    base_url="https://models.inference.ai.azure.com"
)

# ============================================
# STATE
# ============================================
class GraphState(TypedDict):
    query: str
    filters: Dict[str, Any]
    filtered_df: pd.DataFrame
    chart_type: str
    chart_path: str
    explanation: str

# ============================================
# 1️⃣ INTENT AGENT
# ============================================
def intent_agent(state: GraphState):
    query = state["query"]

    prompt = f"""
    Extract parameters from this request:

    "{query}"

    Return JSON:
    {{
        "min_hot": float,
        "min_momentum": float,
        "max_volatility": float,
        "top_n": int,
        "chart_type": "bar" | "heatmap" | "correlation"
    }}
    """

    try:
        response = llm.predict(prompt)
        parsed = json.loads(response)
    except:
        parsed = {
            "min_hot": 0.6,
            "min_momentum": 0.6,
            "max_volatility": 0.7,
            "top_n": 30,
            "chart_type": "bar"
        }

    return {
        "filters": parsed,
        "chart_type": parsed.get("chart_type", "bar")
    }

# ============================================
# 2️⃣ FILTER AGENT
# ============================================
def filter_agent(state: GraphState):
    f = state["filters"]

    filtered = df[
        (df["HotScore"] > f.get("min_hot", 0.5)) &
        (df["MomentumScore"] > f.get("min_momentum", 0.5)) &
        (df["VolatilityScore"] < f.get("max_volatility", 1.0))
    ].sort_values("HotScore", ascending=False)

    filtered = filtered.head(f.get("top_n", 30))

    return {"filtered_df": filtered}

# ============================================
# CHART FUNCTIONS
# ============================================

def generate_bar_chart(df_subset):
    df_subset = df_subset.copy()

    df_subset["score_norm"] = (
        (df_subset["HotScore"] - df_subset["HotScore"].min()) /
        (df_subset["HotScore"].max() - df_subset["HotScore"].min() + 1e-9)
    )

    fig = px.bar(
        df_subset.sort_values("HotScore"),
        x="HotScore",
        y="symbol",
        orientation="h",
        color="score_norm",
        title="Top Hot Stocks"
    )

    path = os.path.join(OUTPUT_DIR, "bar_lang_graph.html")
    fig.write_html(path)
    return path


def generate_heatmap(df_subset):
    metrics = [
        "HotScore", "MomentumScore", "VolumeScore",
        "VolumeSpike", "VolatilityScore", "TrendScore"
    ]

    df_norm = df_subset.copy()

    for col in metrics:
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()
        df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val + 1e-9)

    z = df_norm[metrics].values.T

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=df_norm["symbol"],
        y=metrics,
        colorscale="Blues",
        hovertemplate="Symbol: %{x}<br>Metric: %{y}<br>Value: %{z:.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="Stock Metrics Heatmap",
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    path = os.path.join(OUTPUT_DIR, "heatmap.html")
    fig.write_html(path)
    return path


def generate_correlation(df_subset):
    metrics = [
        "HotScore", "MomentumScore", "VolumeScore",
        "VolumeSpike", "VolatilityScore", "TrendScore"
    ]

    corr = df_subset[metrics].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Feature Correlation"
    )

    path = os.path.join(OUTPUT_DIR, "correlation.html")
    fig.write_html(path)
    return path

# ============================================
# 3️⃣ CHART AGENT
# ============================================
def chart_agent(state: GraphState):
    df_subset = state["filtered_df"]
    chart_type = state["chart_type"]

    if df_subset.empty:
        return {"chart_path": None}

    if chart_type == "heatmap":
        path = generate_heatmap(df_subset)
    elif chart_type == "correlation":
        path = generate_correlation(df_subset)
    else:
        path = generate_bar_chart(df_subset)

    return {"chart_path": path}

# ============================================
# 4️⃣ EXPLAIN AGENT
# ============================================
def explain_agent(state: GraphState):
    df_subset = state["filtered_df"]

    if df_subset.empty:
        return {"explanation": "No stocks matched criteria."}

    sample = df_subset[[
        "symbol","HotScore","MomentumScore","VolumeScore","VolatilityScore"
    ]].to_string()

    prompt = f"""
    Analyze these stocks:

    {sample}

    Provide:
    - Key insights
    - Strongest opportunities
    - Risks
    """

    explanation = llm.predict(prompt)

    return {"explanation": explanation}

# ============================================
# BUILD GRAPH
# ============================================
builder = StateGraph(GraphState)

builder.add_node("intent", intent_agent)
builder.add_node("filter", filter_agent)
builder.add_node("chart", chart_agent)
builder.add_node("explain", explain_agent)

builder.set_entry_point("intent")
builder.add_edge("intent", "filter")
builder.add_edge("filter", "chart")
builder.add_edge("chart", "explain")

graph = builder.compile()

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    user_query = "Show top strong momentum stocks as heatmap"

    result = graph.invoke({
        "query": user_query
    })

    print("\n=== RESULTS ===")
    print("Chart:", result["chart_path"])
    print("\nExplanation:\n", result["explanation"])