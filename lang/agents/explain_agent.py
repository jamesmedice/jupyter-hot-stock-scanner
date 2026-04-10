#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

def explain_agent(state):
    df = state["filtered_df"]

    if df.empty:
        return {"explanation": "No data found."}

    sample = df[
        ["symbol", "HotScore", "MomentumScore", "VolumeScore", "VolatilityScore"]
    ].head(20).to_string()

    prompt = f"""
    Analyze these stocks:

    {sample}

    Provide:
    - Key insights
    - Opportunities
    - Risks
    """

    return {"explanation": llm.predict(prompt)}