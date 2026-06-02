import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging for observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CodeReviewAgent")

# 1. Define the filesystem tool
@tool
def read_local_file(file_path: str) -> str:
    """Reads the contents of a local file and returns it as a string. 
    Use this tool whenever you need to inspect the source code of a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# 2. Initialize the Groq model with verified active identifier
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
model_with_tools = model.bind_tools([read_local_file])

# 3. Build the core evaluation prompt matrix
review_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a comprehensive code reviewer, Enterprise Performance Architect, and Senior Engineer at Auriseg.\n"
        "Your task is to analyze the source code provided to you and critique it strictly across these five pillars:\n"
        "1. Scalability (Concurrency & thread safety under high user traffic)\n"
        "2. Ability to Handle Large Data (Validation of chunking, streaming, or batching)\n"
        "3. Time/Space Complexity (Algorithmic Big-O optimization)\n"
        "4. Error Handling & Observability (Presence of explicit try/except blocks and structured logging)\n"
        "5. Security Defenses (Catching injections, leaks, or resource vulnerabilities)\n\n"
        "Current Running Summary of older conversation context:\n{running_summary}\n\n"
        "Provide your critique using markdown headings for each pillar, followed by '### 🛠️ Refactored Suggestions'."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Here is the code content of the file:\n\n{code_content}")
])

# 4. Initialize stateful memory components
chat_history_buffer = []
running_summary = "No previous conversation history yet."

def generate_summary(current_summary: str, human_msg: str, ai_msg: str) -> str:
    """Background summary calculation."""
    summary_model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    summary_prompt = (
        f"Progressively summarize the conversation. Current Summary: {current_summary}\n"
        f"New interaction to add:\nUser: {human_msg}\nAI: {ai_msg}\n"
        f"Output a concise paragraph updating the running narrative of what has happened so far."
    )
    res = summary_model.invoke(summary_prompt)
    return res.content

print("🚀 Enterprise Agent Session Initialized! Type 'exit' to quit.\n")

# 5. Loop
while True:
    user_query = input("You: ")
    if user_query.lower() == 'exit':
        print("Ending session.")
        break
        
    if not user_query.strip():
        continue

    tool_messages = []
    for msg in chat_history_buffer:
        tool_messages.append(msg)
    tool_messages.append(HumanMessage(content=user_query))
    
    try:
        tool_call_response = model_with_tools.invoke(tool_messages)
    except Exception as e:
        logger.error(f"Error invoking tool prediction model: {str(e)}")
        continue
    
    code_text = ""
    if tool_call_response.tool_calls:
        tool_call = tool_call_response.tool_calls[0]
        if tool_call['name'] == 'read_local_file':
            file_target = tool_call['args'].get('file_path', '')
            print(f"\n📡 [Tool Action] Executing tool: read_local_file on '{file_target}'...")
            code_text = read_local_file.invoke(tool_call['args'])
    else:
        code_text = user_query

    if code_text:
        print("🧠 [LLM Action] Processing conversation context...\n")
        final_chain = review_prompt | model
        try:
            review_output = final_chain.invoke({
                "code_content": code_text,
                "chat_history": chat_history_buffer,
                "running_summary": running_summary
            })
        except Exception as e:
            logger.error(f"Error invoking chain model: {str(e)}")
            continue
        
        print(f"AI:\n{review_output.content}\n")
        
        chat_history_buffer.append(HumanMessage(content=user_query))
        chat_history_buffer.append(AIMessage(content=review_output.content))
        
        if len(chat_history_buffer) > 6:
            print("🗜️ [Memory Action] Compressing old history layer into Summary Memory...")
            old_human = chat_history_buffer.pop(0).content
            old_ai = chat_history_buffer.pop(0).content
            running_summary = generate_summary(running_summary, old_human, old_ai)
            print(f"📝 [Updated Summary Context]: {running_summary}\n")
    else:
        print("AI: Unable to process or retrieve context.\n")
