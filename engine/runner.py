import json

from loader import load_data
from filters import apply_filters
from scoring import compute_scores
from ai_layer import ask_ai
from reporter import save_report

def run(model, items=10):

    df = load_data("ml/runtimes.csv")

    df = apply_filters(df)

    ranked = compute_scores(df)

    top10 = ranked.head(items)

    candidates = top10[
        [
            "symbol",
            "marketCap",
            "VolumeSpike",
            "MomentumScore",
            "VolatilityScore",
            "TrendScore",
            "RuntimeScore",
            "base_score"
        ]
    ].to_dict(orient="records")

    ai_output = ask_ai(candidates, model, items)

    print("AI Output:\n", ai_output)

    report_path = save_report(model, ai_output)

    print("Report saved to:", report_path)