import os

DATA_PATH = "ml/features_base.csv"
OUTPUT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)

MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0