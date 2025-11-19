from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import subprocess
import pytz

def run_daily_stock():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"[{datetime.now()}] Running daily stock scanner...")
    subprocess.run([
        "papermill",
        "02-daily_stock_recommendations_yahoo.ipynb",
        f"output/02_run_{timestamp}.ipynb"
    ])
    print(f"[{datetime.now()}] Finished run.")

scheduler = BlockingScheduler(timezone=pytz.UTC)

# Every 0 and 30 minutes, UTC 14-21, Mon-Fri
scheduler.add_job(
    run_daily_stock,
    'cron',
    day_of_week='mon-fri',
    hour='14-21',
    minute='0,30'
)

print("Scheduler started...")
scheduler.start()
