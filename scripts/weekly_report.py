# scripts/weekly_report.py
import os, glob, re, json, datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DAILY = Path("data/daily")
OUT_WEEKLY = Path("output/weekly")
OUT_WEEKLY.mkdir(parents=True, exist_ok=True)

# Look for files like hot_stocks_YYYYMMDDHHMMSS.csv or daily_top50_YYYYMMDD.csv
files = sorted(DATA_DAILY.glob("hot_stocks_*.csv") | DATA_DAILY.glob("hot_stocks_*.CSV"))
# also consider stable daily_top50 files in output/daily
files += list(Path("output/daily").glob("daily_top50_*.csv"))

# Filter last 7 unique dates by filename date
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

def get_file_date(f):
    m = re.search(r"(\d{8})", f.name)
    if m:
        s = m.group(1)
        return datetime.datetime.strptime(s, "%Y%m%d").date()
    else:
        return None

# collect files with file-date >= seven_days_ago
sel = []
for f in files:
    fd = get_file_date(f)
    if fd and fd >= seven_days_ago and fd <= today:
        sel.append(f)

if not sel:
    print("No daily files for last 7 days found.")
    exit(0)

# load and concat
dfs = []
for f in sel:
    try:
        df = pd.read_csv(f)
        # normalize symbol column name
        if 'symbol' not in df.columns and 'Symbol' in df.columns:
            df = df.rename(columns={'Symbol':'symbol'})
        dfs.append(df.assign(_file=str(f)))
    except Exception as e:
        print("Read error", f, e)

all_df = pd.concat(dfs, ignore_index=True, sort=False)

# aggregated stats per symbol
agg = all_df.groupby("symbol").agg(
    appearances=("symbol","count"),
    avg_HotScore=("HotScore","mean"),
    median_HotScore=("HotScore","median"),
    avg_vol_spike=("VolumeSpike","mean"),
    avg_mom_pct=("regularMarketChangePercent","mean")
).sort_values(["appearances","avg_HotScore"], ascending=False)

weekly_csv = OUT_WEEKLY / f"weekly_summary_{today.strftime('%Y%m%d')}.csv"
agg.to_csv(weekly_csv)
print("Saved:", weekly_csv)

# heatmap across days: pivot symbol x date with mean HotScore
all_df['date'] = all_df['_file'].apply(lambda x: (re.search(r"(\d{8})", Path(x).name).group(1) if re.search(r"(\d{8})", Path(x).name) else None))
pivot = all_df.pivot_table(index='symbol', columns='date', values='HotScore', aggfunc='mean').fillna(0)

heatmap_file = OUT_WEEKLY / f"weekly_heatmap_{today.strftime('%Y%m%d')}.png"
plt.figure(figsize=(12, max(6, 0.12*len(pivot))))
plt.imshow(pivot.values, aspect='auto', cmap='YlOrRd')
plt.yticks(range(len(pivot)), pivot.index)
plt.xticks(rotation=45)
plt.colorbar(label='HotScore')
plt.title("Weekly HotScore Heatmap")
plt.tight_layout()
plt.savefig(heatmap_file, dpi=200)
plt.close()
print("Saved:", heatmap_file)

# metadata
meta = {
    "generated": datetime.datetime.now().isoformat(),
    "files_used": [str(x) for x in sel],
    "rows": len(all_df),
    "unique_symbols": all_df['symbol'].nunique()
}
meta_file = OUT_WEEKLY / f"weekly_metadata_{today.strftime('%Y%m%d')}.json"
with open(meta_file, "w") as fh:
    json.dump(meta, fh, indent=2)
print("Saved:", meta_file)
