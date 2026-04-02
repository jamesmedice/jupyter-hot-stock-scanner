import json

from loader import load_data
from filters import apply_filters
from scoring import compute_scores
from ai_layer import ask_ai
from reporter import save_report
import runner

MODEL = 'ai21-labs/AI21-Jamba-1.5-Large'

if __name__ == "__main__":
    runner.run(model=MODEL)