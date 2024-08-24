# coding: utf-8

from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from agent.rag.graph.state import AgentState
from agent.rag.graph.nodes import agentFunc, rewriteFunc, generateFunc
from agent.rag.graph.edges import gradeFunc

def build_graph(llm, tools):
    # Define a new graph
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("agent", agentFunc(llm, tools))
    workflow.add_node("retrieve", ToolNode(tools))
    workflow.add_node("rewrite", rewriteFunc(llm))
    workflow.add_node("generate", generateFunc(llm))
    
    # Edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "retrieve",
            END: END,
        },
    )
    workflow.add_conditional_edges(
        "retrieve",
        gradeFunc(llm),
    )
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")

    # Compile
    return workflow.compile()
