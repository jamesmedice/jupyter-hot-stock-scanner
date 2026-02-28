def compute_scores(df):
    df = df.copy()

    df["acceleration"] = df["HotScore_today"] - df["HotScore_avg"]

    df["base_score"] = (
        0.3  * df["RuntimeScore"] +
        0.2  * df["MomentumScore"] +
        0.15 * df["VolumeSpike"] +
        0.15 * df["TrendScore"] +
        0.1  * df["acceleration"] +
        0.1  * (df["regularMarketChangePercent"] / 100) -  # scale %
        0.1  * df["VolatilityScore"]
    )

    return df.sort_values("base_score", ascending=False)