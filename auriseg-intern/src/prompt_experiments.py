import logging
import sys
import math
import requests
import re
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging for observability
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("CodeReviewAgent")

# --- MODEL CONFIGURATION ---
MODEL_NAME = "llama-3.3-70b-versatile"

# 1. Native Python Tool Execution Blocks
def read_local_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            return f"\n--- Contents of {file_path} ---\n{f.read()}\n"
    except Exception as e:
        return f"\n[File Error] Could not read '{file_path}': {str(e)}\n"

def web_search_tool(query: str) -> str:
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = response.json()
        
        abstract = data.get("AbstractText", "")
        if abstract:
            return f"\n[Search Result for '{query}']: {abstract}\n"
        
        topics = data.get("RelatedTopics", [])
        if topics and "Text" in topics[0]:
            return f"\n[Search Result for '{query}']: {topics[0]['Text']}\n"
            
        return f"\n[Search Result]: No direct summary found for '{query}'.\n"
    except Exception as e:
        return f"\n[Search Error] Operational issue: {str(e)}\n"

def calculator(expression: str) -> str:
    try:
        # Clean expression for calculation
        expr_clean = expression.replace('?', '').strip()
        allowed_names = {
            'abs': abs, 'round': round, 'max': max, 'min': min, 'sum': sum,
            'pow': pow, 'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
            'tan': math.tan, 'pi': math.pi, 'e': math.e
        }
        result = eval(expr_clean, {"__builtins__": None}, allowed_names)
        return f"\n[Calculation Result]: {expression} = {result}\n"
    except Exception as e:
        return f"\n[Calculator Error] Failed to evaluate '{expression}': {str(e)}\n"

# 2. Initialize Core Model
try:
    model = ChatGroq(model=MODEL_NAME, temperature=0)
except Exception as e:
    logger.error(f"Failed to initialize Groq model: {str(e)}")
    sys.exit(1)

# 3. Standard 5 Pillars Evaluation Matrix
review_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a comprehensive code reviewer, Enterprise Performance Architect, and Senior Engineer at Auriseg.\n"
        "Analyze the provided context or content and critique it strictly across these five pillars:\n"
        "1. Scalability (Concurrency & safety)\n"
        "2. Ability to Handle Large Data (Streaming/chunking validation)\n"
        "3. Time/Space Complexity (Algorithmic Big-O optimization)\n"
        "4. Error Handling & Observability (Try/except blocks and structured logs)\n"
        "5. Security Defenses (Catching leaks or vulnerabilities)\n\n"
        "If the context contains a mix of file data, search calculations, and text, focus your core code review "
        "on the file contents, while cleanly addressing the other answers at the very end under an '### ℹ️ Miscellaneous Queries' section."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "Here is the collected system context:\n\n{code_content}")
])

# 4. State Buffers
chat_history_buffer = []

print("🚀 Enterprise Multi-Tool Agent Initialized! Type 'exit' to quit.\n")

# 5. Interactive Loop with Smart Multi-Intent Aggregation
while True:
    try:
        user_query = input("You: ")
        if user_query.lower() == 'exit':
            print("Ending session.")
            break
            
        if not user_query.strip():
            continue

        collected_context = ""
        tools_triggered = []

        # 🔍 Intent Extraction Pattern 1: Calculator
        if re.search(r'[\d\s()+\-*/=]{3,}', user_query) and any(char in user_query for char in ['+', '-', '*', '/']):
            math_match = re.search(r'([\d\s()+\-*/]{3,}\d)', user_query)
            if math_match:
                expr = math_match.group(1).strip()
                print(f"📡 [Tool Action] Executing math engine...")
                calc_res = calculator(expr)
                collected_context += calc_res
                tools_triggered.append(calc_res)

        # 🔍 Intent Extraction Pattern 2: Local File Reader
        if "file" in user_query.lower() or "read" in user_query.lower():
            file_match = re.search(r'([a-zA-Z0-9_\-/]+\.[a-zA-Z0-9]+)', user_query)
            if file_match:
                path = file_match.group(1)
                print(f"📡 [Tool Action] Reading local path '{path}'...")
                file_res = read_local_file(path)
                collected_context += file_res

        # 🔍 Intent Extraction Pattern 3: Web Search Lookups
        if any(keyword in user_query.lower() for keyword in ["where is", "capital city of", "who won", "uganda", "afghanistan"]):
            search_target = ""
            if "uganda" in user_query.lower(): search_target = "Uganda capital city"
            elif "afghanistan" in user_query.lower(): search_target = "Afghanistan capital city"
            else: search_target = user_query
            
            print(f"📡 [Tool Action] Querying Web Search API...")
            search_res = web_search_tool(search_target)
            collected_context += search_res
            tools_triggered.append(search_res)

        # Fallback if no specific template patterns were matched
        if not collected_context:
            collected_context = user_query

        # 🔥 SMART BYPASS: If tools ran but NO code files were targets, summarize clean facts!
        if tools_triggered and not ("file" in user_query.lower() or "review" in user_query.lower()):
            print(f"\n🧠 [LLM Action] Synthesizing final response...")
            summary_prompt = (
                f"You are a helpful engineering assistant. Address the user's initial inputs directly using "
                f"the compiled tool outputs provided below. Keep it concise, professional, and clear.\n\n"
                f"User Request: {user_query}\n"
                f"Tool Outputs:\n{collected_context}"
            )
            ans = model.invoke(summary_prompt)
            print(f"\nAI:\n{ans.content}\n")
            print("-" * 40)
            chat_history_buffer.append(HumanMessage(content=user_query))
            chat_history_buffer.append(AIMessage(content=ans.content))
            continue

        # Run the full unified multi-context through the 5 Pillars Architecture Matrix
        print("🧠 [LLM Action] Processing multi-intent context through 5 Pillars...\n")
        final_chain = review_prompt | model
        review_output = final_chain.invoke({
            "code_content": collected_context,
            "chat_history": chat_history_buffer[-4:]
        })
        
        print(f"AI:\n{review_output.content}\n")
        print("-" * 40)
        
        chat_history_buffer.append(HumanMessage(content=user_query))
        chat_history_buffer.append(AIMessage(content=review_output.content))
        
    except KeyboardInterrupt:
        print("\nSession interrupted cleanly.")
        continue
    except Exception as e:
        print(f"\n❌ Loop encountered error: {str(e)}\n")
        continue
