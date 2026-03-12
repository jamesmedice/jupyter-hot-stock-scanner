import json

from loader import load_data
from filters import apply_filters
from scoring import compute_scores
from ai_layer import ask_ai
from reporter import save_report
import runner

MODEL = 'meta/Meta-Llama-3.1-405B-Instruct'

if __name__ == "__main__":
    runner.run(model=MODEL)