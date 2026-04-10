import json
import os
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE


token = os.environ["GITHUB_TOKEN"] 
llm = ChatOpenAI(model=MODEL_NAME, api_key=token, temperature=TEMPERATURE, base_url="https://models.inference.ai.azure.com")

def intent_agent(state):
    query = state["query"]

    prompt = f"""
    Extract trading parameters from:

    "{query}"
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
        **state,   # 👈 CRITICAL FIX
        "filters": parsed,
        "chart_type": parsed.get("chart_type", "bar")
    }