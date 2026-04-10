import json
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

def intent_agent(state):
    query = state["query"]

    prompt = f"""
    Extract trading parameters from:

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
        "chart_type": parsed["chart_type"]
    }