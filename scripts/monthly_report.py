# scripts/monthly_report.py
import os, glob, re, json, datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DAILY = Path("data/daily")
OUT_MONTHLY = Path("output/monthly")
OUT_MONTHLY.mkdir(parents=True, exist_ok=True)

today = datetime.date.today()
start_date = today - datetime.timedelta(days=30)

def get_file_date(f):
    m = re.search(r"(\d{8})", f.name)
    if m:
        s = m.group(1)
        return datetime.datetime.strptime(s, "%Y%m%d").date()
    else:
        return None

files = list(DATA_DAILY.glob("hot_stocks_*.csv")) + list(Path("output/daily").glob("daily_top50_*.csv"))
sel = [f for f in files if (get_file_date(f) and start_date <= get_file_date(f) <= today)]
if not sel:
    print("No files for last 30 days.")
    exit(0)

dfs = []
for f in sel:
    try:
        df = pd.read_csv(f)
        if 'symbol' not in df.columns and 'Symbol' in df.columns:
            df = df.rename(columns={'Symbol':'symbol'})
        dfs.append(df.assign(_file=str(f)))
    except Exception as e:
        print("Read error", f, e)

all_df = pd.concat(dfs, ignore_index=True, sort=False)

agg = all_df.groupby("symbol").agg(
    appearances=("symbol","count"),
    avg_HotScore=("HotScore","mean"),
    avg_vol_spike=("VolumeSpike","mean"),
    avg_mom_pct=("regularMarketChangePercent","mean")
).sort_values("avg_HotScore", ascending=False)

monthly_csv = OUT_MONTHLY / f"monthly_summary_{today.strftime('%Y%m%d')}.csv"
agg.to_csv(monthly_csv)
print("Saved:", monthly_csv)

# heatmap
all_df['date'] = all_df['_file'].apply(lambda x: (re.search(r"(\d{8})", Path(x).name).group(1) if re.search(r"(\d{8})", Path(x).name) else None))
pivot = all_df.pivot_table(index='symbol', columns='date', values='HotScore', aggfunc='mean').fillna(0)

heatmap_file = OUT_MONTHLY / f"monthly_heatmap_{today.strftime('%Y%m%d')}.png"
plt.figure(figsize=(12, max(6, 0.1*len(pivot))))
plt.imshow(pivot.values, aspect='auto', cmap='YlOrRd')
plt.yticks(range(len(pivot)), pivot.index)
plt.xticks(rotation=45)
plt.colorbar(label='HotScore')
plt.title("Monthly HotScore Heatmap")
plt.tight_layout()
plt.savefig(heatmap_file, dpi=200)
plt.close()
print("Saved:", heatmap_file)

meta = {
    "generated": datetime.datetime.now().isoformat(),
    "files_used": [str(x) for x in sel],
    "rows": len(all_df),
    "unique_symbols": all_df['symbol'].nunique()
}
meta_file = OUT_MONTHLY / f"monthly_metadata_{today.strftime('%Y%m%d')}.json"
with open(meta_file, "w") as fh:
    json.dump(meta, fh, indent=2)
print("Saved:", meta_file)
