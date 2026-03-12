import json

from loader import load_data
from filters import apply_filters
from scoring import compute_scores
from ai_layer import ask_ai
from reporter import save_report
import runner

MODEL_GROK = 'gpt-5-mini'

if __name__ == "__main__":
    runner.run(model=MODEL_GROK)