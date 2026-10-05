from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.redis import RedisSaver

from .state import AgentState
from .planner import create_plan

from .tools import (
    ats_tool,
    skill_match_tool,
    rewrite_tool,
    interview_tool
)


tools = {
    "ats": ats_tool,
    "skills": skill_match_tool,
    "rewrite": rewrite_tool,
    "interview": interview_tool
}


def planner_node(state):

    state["plan"] = create_plan(
        state["user_query"],
        state.get("results", {})
    )    
    state["current_step"] = 0

    return state


def execute_tool(state):

    step = state["plan"][state["current_step"]]

    print("PLAN:", state["plan"])
    print("CURRENT STEP:", state["current_step"])
    print("EXECUTING:", step)
    print("STATE KEYS BEFORE:", state.keys())

    tool = tools[step]

    state = tool(state)

    print("STATE KEYS AFTER:", state.keys())

    state["current_step"] += 1

    return state


def should_continue(state):

    if state["current_step"] >= len(state["plan"]):
        return "final"

    return "execute"

def final_node(state):
    return {
        "results": state["results"]
    }


graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)

graph.add_node("execute", execute_tool)

graph.add_edge(START, "planner")

graph.add_edge("planner", "execute")

graph.add_node("final", final_node)

graph.add_conditional_edges(
    "execute",
    should_continue,
    {
        "execute": "execute",
        "final": "final"
    }
)

graph.add_edge("final", END)

from langgraph.checkpoint.redis import RedisSaver

checkpointer = RedisSaver(
    redis_url="redis://localhost:6379"
)

checkpointer.setup()

agent = graph.compile(
    checkpointer=checkpointer
)