def filter_agent(state):
    df = state["df"]
    f = state["filters"]

    filtered = df[
        (df["HotScore"] > f.get("min_hot", 0.5)) &
        (df["MomentumScore"] > f.get("min_momentum", 0.5)) &
        (df["VolatilityScore"] < f.get("max_volatility", 1.0))
    ].sort_values("HotScore", ascending=False)

    return {
        "filtered_df": filtered.head(f.get("top_n", 30))
    }