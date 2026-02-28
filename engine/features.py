import pandas as pd
import numpy as np

def engineer_features(df):
    df = df.copy()

    df["return_1h"] = df["close"].pct_change()
    df["momentum_3h"] = df["close"].pct_change(3)
    df["rel_volume"] = df["volume"] / df["volume"].rolling(20).mean()
    df["volatility"] = df["close"].pct_change().rolling(10).std()

    df = df.dropna()
    return df