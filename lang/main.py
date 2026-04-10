from data_loader import load_data
from graph.builder import build_graph

def main():
    df = load_data()
    graph = build_graph()

    query = "Show top momentum low volatility stocks as heatmap"

    result = graph.invoke({
        "query": query,
        "df": df
    })

    print("\n=== OUTPUT ===")
    print("Chart:", result.get("chart_path"))
    print("Explanation:\n", result.get("explanation"))

if __name__ == "__main__":
    main()