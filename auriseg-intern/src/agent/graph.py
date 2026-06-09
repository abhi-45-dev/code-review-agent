from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState

from src.agent.nodes.ingest_node import ingest_node
from src.agent.nodes.retrieve_node import retrieve_node
from src.agent.nodes.bug_node import bug_node
from src.agent.nodes.quality_node import quality_node
from src.agent.nodes.security_node import security_node
from src.agent.nodes.improve_node import improve_node
from src.agent.nodes.report_node import report_node


builder = StateGraph(AgentState)

builder.add_node("ingest", ingest_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("bug", bug_node)
builder.add_node("quality", quality_node)
builder.add_node("security", security_node)
builder.add_node("improve", improve_node)
builder.add_node("report", report_node)

builder.add_edge(START, "ingest")
builder.add_edge("ingest", "retrieve")

# Parallel execution
builder.add_edge("retrieve", "bug")
builder.add_edge("retrieve", "quality")
builder.add_edge("retrieve", "security")
builder.add_edge("retrieve", "improve")

# Merge
builder.add_edge("bug", "report")
builder.add_edge("quality", "report")
builder.add_edge("security", "report")
builder.add_edge("improve", "report")

builder.add_edge("report", END)

graph = builder.compile()
