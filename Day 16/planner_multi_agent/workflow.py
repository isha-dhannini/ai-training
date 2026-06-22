import os
import json
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Define structural agent state schema
class AgentState(TypedDict):
    goal: str
    tasks: List[str]
    results: List[str]
    critique: str
    iterations: int
    approved: bool

# Initialize Llama 3.1 via Groq
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# --- Agent Node 1: Planner ---
def planner(state: AgentState) -> AgentState:
    system = """You are a planning agent. Break the user's goal into
at most 5 concrete, actionable tasks. Respond ONLY with a
valid JSON array of strings. No preamble, no markdown."""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=f"Goal: {state['goal']}")
    ]
    response = llm.invoke(messages).content.strip()

    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        tasks = json.loads(clean)
    except Exception:
        tasks = [response]  # Fallback payload

    return {**state, "tasks": tasks}

# --- Agent Node 2: Executor ---
search = DuckDuckGoSearchRun()

def executor(state: AgentState) -> AgentState:
    results = []
    critique_ctx = ""
    if state.get("critique"):
        critique_ctx = f"\n\nYour previous attempt was rejected. Previous critique: {state['critique']}"

    for task in state["tasks"]:
        system = f"""You are an execution agent. Complete the task thoroughly. Use web search if you need
current information. {critique_ctx}"""

        search_ctx = ""
        try:
            search_result = search.run(task[:100])
            search_ctx = f"\n\nWeb search result for context: \n{search_result[:800]}"
        except Exception:
            pass

        messages = [
            SystemMessage(content=system),
            HumanMessage(content=f"Task: {task}{search_ctx}")
        ]

        result = llm.invoke(messages).content
        results.append(result)
        
    return {**state, "results": results, "iterations": state["iterations"] + 1}

# --- Agent Node 3: Verifier ---
def verifier(state: AgentState) -> AgentState:
    # Safety valve: force auto-approve on max iteration boundaries
    if state["iterations"] >= 3:
        return {**state, "approved": True}

    combined_results = "\n\n".join(
        f"Task {i+1}: {t}\nResult: {r}"
        for i, (t, r) in enumerate(zip(state["tasks"], state["results"]))
    )
    
    system = """You are a quality verifier. Evaluate the results against the
original goal using this rubric:
- Completeness: Does it fully address the goal? (0-0.4)
- Accuracy:     Is the information correct and specific? (0-0.3)
- Clarity:      Is it well-structured and clear? (0-0.3)
Sum the scores for a total between 0.0 and 1.0.
Respond ONLY as valid JSON: {"score":0.9, "completeness_score": 0.35, "accuracy_score": 0.2, "clarity_score":0.15, "approved": true, "critique": "..."}"""

    messages = [
        SystemMessage(content=system),
        HumanMessage(content=f"Original goal: {state['goal']}\n\nResults:\n{combined_results}")
    ]
    
    raw = llm.invoke(messages).content.strip()
    try:
        clean = raw.replace("```json", "").replace("```", "").strip()
        verdict = json.loads(clean)
        approved = verdict.get("approved", False)
        critique = verdict.get("critique", "")
    except Exception:
        approved, critique = False, raw

    return {**state, "approved": approved, "critique": critique}

# --- Conditional Edge Router ---
def route_after_verify(state: AgentState) -> str:
    return "end" if state.get("approved") else "executor"

# --- Compilation Function ---
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("verifier", verifier)

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "verifier")

    graph.add_conditional_edges(
        "verifier",
        route_after_verify,
        {
            "end": END,
            "executor": "executor"
        }
    )

    graph.set_entry_point("planner")
    return graph.compile()