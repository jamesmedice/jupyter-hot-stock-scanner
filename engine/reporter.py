from datetime import datetime
import os

def save_report(content: str):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    path = f"reports/{timestamp}-report.md"

    with open(path, "w") as f:
        f.write(f"# Hourly Stock Report - {timestamp} UTC\n\n")
        f.write(content)

    return path