from datetime import datetime
import os

def sanitize_filename(name: str) -> str:
    return name.replace("/", "_")

def save_report(model, content: str):

    safe_model = sanitize_filename(model)
    path = f"reports/{safe_model}.html"

    os.makedirs("reports", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path