from typing import TypedDict, Dict, Any
import pandas as pd


class GraphState(TypedDict, total=False):
    query: str
    df: pd.DataFrame
    filters: Dict[str, Any]
    filtered_df: pd.DataFrame
    chart_type: str
    chart_path: str
    explanation: str