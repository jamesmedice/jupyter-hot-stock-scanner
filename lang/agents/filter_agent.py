def filter_agent(state):
    df = state["df"]
    f = state["filters"]

    min_hot = max(0.0, min(f.get("min_hot", 0.5), 1.0))
    min_mom = max(0.0, min(f.get("min_momentum", 0.5), 1.0))
    max_vol = max(0.1, min(f.get("max_volatility", 1.0), 1.0))
    top_n = max(1, min(f.get("top_n", 30), 100))

    filtered = df[
        (df["HotScore"] > min_hot) &
        (df["MomentumScore"] > min_mom) &
        (df["VolatilityScore"] < max_vol)
    ]

    if filtered.empty:
        print("⚠️ No results — relaxing volatility")
        filtered = df[
            (df["HotScore"] > min_hot) &
            (df["MomentumScore"] > min_mom)
        ]

    if filtered.empty:
        print("⚠️ Still empty — using top stocks")
        filtered = df

    filtered = filtered.sort_values("HotScore", ascending=False)

    return {
        "filtered_df": filtered.head(top_n)
    }