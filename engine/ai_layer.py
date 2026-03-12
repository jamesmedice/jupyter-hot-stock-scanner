import os
import json
from openai import OpenAI

def ask_ai(candidates, model="grok-3-mini", items=10):

    client = OpenAI(
        api_key=os.environ["GITHUB_TOKEN"],
        base_url="https://models.github.ai/inference"
    )

    payload = json.dumps(candidates, indent=2)

    print(f"Payload sent to AI: {payload}")    

    response = client.chat.completions.create(
        model=model,  
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
                    "4) Return the top {items} symbols "
                    "5) Provide concise reasoning per stock in html."
                )
            },
            {
                "role": "user",
                "content": payload
            }
        ]
    )

    return response.choices[0].message.content