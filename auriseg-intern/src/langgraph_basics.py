from typing import TypedDict
from langgraph.graph import StateGraph, END

# ==========================================
# SECTION 1: DEFINE THE STATE (Data Schema)
# ==========================================
class PipelineState(TypedDict):
    input_text: str
    is_valid: bool


# ==========================================
# SECTION 2: DEFINE THE NODES (Execution Functions)
# ==========================================
def process_text_node(state: PipelineState) -> dict:
    print("🤖 [Node 1] Processing text...")
    text_value = state["input_text"]
    
    # Text becomes valid if it contains the word "apple"
    check_valid = "apple" in text_value.lower()
    
    return {
        "input_text": text_value.upper(),
        "is_valid": check_valid
    }

def success_node(state: PipelineState) -> dict:
    print("✅ [Node 2] Success path triggered!")
    return {
        "input_text": state["input_text"] + " -> PASSED!"
    }

def fallback_node(state: PipelineState) -> dict:
    print("❌ [Node 3] Fallback path triggered!")
    return {
        "input_text": state["input_text"] + " -> FAILED!"
    }


# ==========================================
# SECTION 3 & 4: BUILDING AND ROUTING (Edges)
# ==========================================
# Initialize the blueprint matrix
builder = StateGraph(PipelineState)

# Register our Python functions as structural system Nodes
builder.add_node("process_step", process_text_node)
builder.add_node("success_step", success_node)
builder.add_node("fallback_step", fallback_node)

# Define the entrance point of the data pipeline
builder.set_entry_point("process_step")

# Traffic cop function to evaluate variables right after Node 1 completes
def routing_logic(state: PipelineState) -> str:
    if state["is_valid"]:
        return "go_to_success"
    else:
        return "go_to_fallback"

# Map the router output to conditional execution roads
builder.add_conditional_edges(
    "process_step",
    routing_logic,
    {
        "go_to_success": "success_step",
        "go_to_fallback": "fallback_step"
    }
)

# Connect final operational processing steps to the system END marker
builder.add_edge("success_step", END)
builder.add_edge("fallback_step", END)


# ==========================================
# SECTION 5: COMPILE AND EXECUTE
# ==========================================
# Turn the blueprint into an active runnable instance application
compiled_graph = builder.compile()

print("🚀 LangGraph 3-Node Blueprint Compiled Successfully!\n")
print("-" * 60)

# --- TEST RUN 1: This input contains "apple" (Should pass) ---
print("🏃 Running Test 1 (Passing Condition)...")
initial_state_1 = {
    "input_text": "I love eating a crunchy apple in the morning",
    "is_valid": False
}
output_1 = compiled_graph.invoke(initial_state_1)
print(f"📥 Input Text:  '{initial_state_1['input_text']}'")
print(f"📤 Output Text: '{output_1['input_text']}'\n")

print("-" * 60)

# --- TEST RUN 2: This input does NOT contain "apple" (Should fail) ---
print("🏃 Running Test 2 (Fallback Condition)...")
initial_state_2 = {
    "input_text": "This text contains ordinary words",
    "is_valid": False
}
output_2 = compiled_graph.invoke(initial_state_2)
print(f"📥 Input Text:  '{initial_state_2['input_text']}'")
print(f"📤 Output Text: '{output_2['input_text']}'\n")
