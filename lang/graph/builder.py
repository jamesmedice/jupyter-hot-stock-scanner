from langgraph.graph import StateGraph

from agents.intent_agent import intent_agent
from agents.filter_agent import filter_agent
from agents.chart_agent import chart_agent
from agents.explain_agent import explain_agent

from state import GraphState


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("intent", intent_agent)
    builder.add_node("filter", filter_agent)
    builder.add_node("chart", chart_agent)
    builder.add_node("explain", explain_agent)

    builder.set_entry_point("intent")

    builder.add_edge("intent", "filter")
    builder.add_edge("filter", "chart")
    builder.add_edge("chart", "explain")

    return builder.compile()