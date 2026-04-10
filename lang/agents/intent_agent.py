import json
import os
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE


token = os.environ["GITHUB_TOKEN"] 
llm = ChatOpenAI(model=MODEL_NAME, api_key=token, temperature=TEMPERATURE, base_url="https://models.inference.ai.azure.com")
 
def intent_agent(state):
    query = state["query"]

    prompt = f"""
    Return ONLY valid JSON.

    DO NOT include markdown, stars, or explanations.

    Format:
    {{
        "min_hot": float (0–1),
        "min_momentum": float (0–1),
        "max_volatility": float (0–1),
        "top_n": int,
        "chart_type": "bar" | "heatmap" | "correlation"
    }}

    Query:
    "{query}"
    """

    try:
        response = llm.invoke(prompt).content
        print("LLM RESPONSE:", response)
        parsed = json.loads(response)

    except Exception as e:
        print("Parsing failed:", e)

        # 🔥 fallback based on query keywords (important)
        chart_type = "bar"
        if "heatmap" in query.lower():
            chart_type = "heatmap"
        elif "correlation" in query.lower():
            chart_type = "correlation"

        parsed = {
            "min_hot": 0.6,
            "min_momentum": 0.6,
            "max_volatility": 0.7,
            "top_n": 30,
            "chart_type": chart_type
        }

    return {
        **state,
        "filters": parsed,
        "chart_type": parsed.get("chart_type", "bar")
    }