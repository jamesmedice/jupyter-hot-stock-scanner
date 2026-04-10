import os
from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE


token = os.environ["GITHUB_TOKEN"]
llm = ChatOpenAI(model=MODEL_NAME, api_key=token, temperature=TEMPERATURE, base_url="https://models.inference.ai.azure.com")

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