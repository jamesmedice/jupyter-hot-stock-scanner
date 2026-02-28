from loader import load_data
from filters import apply_filters
from scoring import compute_scores
from ai_layer import ask_ai
from reporter import save_report

def run():

    df = load_data("../ml/runtimes.csv")

    df = apply_filters(df)

    ranked = compute_scores(df)

    top50 = ranked.head(50)

    candidates = top50[
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


    ai_output = ask_ai(candidates)

    report_path = save_report(ai_output)

    print("Report saved to:", report_path)


if __name__ == "__main__":
    run()