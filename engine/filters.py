

def apply_filters(df):
    df = df[
        (df["marketCap"] > 2_000_000_000) &
        (df["regularMarketVolume"] > 500_000) &
        (df["VolumeSpike"] > 1.1)
    ]
    return df