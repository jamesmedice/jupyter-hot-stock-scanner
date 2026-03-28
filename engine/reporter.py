from datetime import datetime
import os

def sanitize_filename(name: str) -> str:
    return name.replace("/", "_")

def save_report(model, content: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

    safe_model = sanitize_filename(model)
    path = f"reports/{safe_model}.html"

    os.makedirs("reports", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"<h1>Hourly Stock Report - {timestamp} UTC</h1>\n")
        f.write(content)

    return path