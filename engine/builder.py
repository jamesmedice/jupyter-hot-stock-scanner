def build_messages(payload, items):

    system_prompt = f"""
You are a professional quantitative risk auditor.

You receive stock metrics in JSON format.

Your task:
1. Remove unstable pump candidates
2. Penalize extreme volatility
3. Favor liquid large-cap breakouts
4. Return the top {items} symbols
5. Provide concise reasoning per stock

Output rules:
- Respond ONLY in Markdown
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