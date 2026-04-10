# ===============================
# IMPORTS
# ===============================
import pandas as pd
import plotly.express as px
from typing import TypedDict, List, Dict, Any

#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph


# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("ml/features_base.csv")
# ===============================
# LLM
# ===============================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ===============================
# STATE DEFINITION
# ===============================
class GraphState(TypedDict):
    query: str
    filters: Dict[str, Any]
    filtered_df: Any
    chart_path: str
    explanation: str

# ===============================
# 1️⃣ INTENT AGENT
# ===============================
def intent_agent(state: GraphState):
    query = state["query"]

    prompt = f"""
    Extract filtering parameters from this query:

    "{query}"

    Return JSON with:
    - min_hot
    - min_momentum
    - max_volatility
    - top_n
    """

    response = llm.predict(prompt)

    try:
        filters = eval(response)  # quick parse (later use json.loads)
    except:
        filters = {
            "min_hot": 0.6,
            "min_momentum": 0.6,
            "max_volatility": 0.7,
            "top_n": 20
        }

    return {"filters": filters}

# ===============================
# 2️⃣ FILTER AGENT (PANDAS)
# ===============================
def filter_agent(state: GraphState):
    f = state["filters"]

    filtered = df[
        (df["HotScore"] > f.get("min_hot", 0.5)) &
        (df["MomentumScore"] > f.get("min_momentum", 0.5)) &
        (df["VolatilityScore"] < f.get("max_volatility", 1.0))
    ].sort_values("HotScore", ascending=False)

    top_n = f.get("top_n", 20)
    filtered = filtered.head(top_n)

    return {"filtered_df": filtered}

# ===============================
# 3️⃣ CHART AGENT
# ===============================
def chart_agent(state: GraphState):
    df_subset = state["filtered_df"].copy()

    if df_subset.empty:
        return {"chart_path": None}

    df_subset["score_norm"] = (
        (df_subset["HotScore"] - df_subset["HotScore"].min()) /
        (df_subset["HotScore"].max() - df_subset["HotScore"].min())
    )

    fig = px.bar(
        df_subset.sort_values("HotScore"),
        x="HotScore",
        y="symbol",
        orientation="h",
        color="score_norm",
        title="AI Generated Stock Chart"
    )

    path = "reports/langchain.html"
    fig.write_html(path)

    return {"chart_path": path}

# ===============================
# 4️⃣ EXPLANATION AGENT
# ===============================
def explain_agent(state: GraphState):
    df_subset = state["filtered_df"]

    if df_subset.empty:
        return {"explanation": "No stocks matched the criteria."}

    sample = df_subset[[
        "symbol","HotScore","MomentumScore","VolumeScore","VolatilityScore"
    ]].to_string()

    prompt = f"""
    Analyze these stocks:

    {sample}

    Provide:
    - Key patterns
    - Top opportunities
    - Risks
    """

    explanation = llm.predict(prompt)

    return {"explanation": explanation}

# ===============================
# BUILD GRAPH
# ===============================
builder = StateGraph(GraphState)

builder.add_node("intent", intent_agent)
builder.add_node("filter", filter_agent)
builder.add_node("chart", chart_agent)
builder.add_node("explain", explain_agent)

# FLOW
builder.set_entry_point("intent")
builder.add_edge("intent", "filter")
builder.add_edge("filter", "chart")
builder.add_edge("chart", "explain")

graph = builder.compile()

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    user_query = "Find high momentum low volatility stocks and show chart"

    result = graph.invoke({
        "query": user_query
    })

    print("\n=== RESULTS ===")
    print("Chart:", result["chart_path"])
    print("Explanation:\n", result["explanation"])