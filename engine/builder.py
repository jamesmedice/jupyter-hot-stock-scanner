def build_messages(payload, items):

    system_prompt = f"""
You are a professional quantitative risk auditor.

You receive stock metrics in JSON format.

Your task:
1. Favor liquid large-cap breakouts
2. Return the top {items} symbols
3. Provide concise reasoning per stock

Output rules:
- Respond in HTML rich in CSS with blue, green, colors with shade
- Include a ranked list
- Each stock must include a short reasoning paragraph
"""

    return [
        {
            "role": "system",
            "content": system_prompt.strip()
        },
        {
            "role": "user",
            "content": payload
        }
    ]