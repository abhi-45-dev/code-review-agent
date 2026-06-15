from langgraph.graph import StateGraph, START, END

from src.agent.state import AgentState

from src.agent.nodes.ingest_node import ingest_node
from src.agent.nodes.retrieve_node import retrieve_node
from src.agent.nodes.review_node import review_node
from src.agent.nodes.report_node import report_node
from src.agent.nodes.router_node import (
    route_next_file,
    has_more_files
)

builder = StateGraph(AgentState)

builder.add_node("ingest", ingest_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("review", review_node)
builder.add_node("report", report_node)
builder.add_node("route_next_file", route_next_file)

builder.add_edge(START, "ingest")

builder.add_edge("ingest", "retrieve")

builder.add_edge("retrieve", "review")

builder.add_edge("review", "report")

builder.add_conditional_edges(
    "report",
    has_more_files,
    {
        "next": "route_next_file",
        "end": END
    }
)

builder.add_edge(
    "route_next_file",
    "retrieve"
)

graph = builder.compile()
