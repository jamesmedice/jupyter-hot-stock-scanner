import os
import json
from openai import OpenAI

def ask_ai(candidates):

    client = OpenAI(
        api_key=os.environ["GITHUB_TOKEN"],
        base_url="https://models.github.ai/inference"
    )

    payload = json.dumps(candidates, indent=2)

    response = client.chat.completions.create(
        model="gpt-5",  # replace with exact slug from GitHub marketplace
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional quantitative risk auditor. "
                    "Given stock metrics in JSON format: "
                    "1) Remove unstable pump candidates "
                    "2) Penalize extreme volatility "
                    "3) Favor liquid large-cap breakouts "
                    "4) Return the top 20 symbols "
                    "5) Provide concise reasoning per stock."
                )
            },
            {
                "role": "user",
                "content": payload
            }
        ]
    )

    return response.choices[0].message.content