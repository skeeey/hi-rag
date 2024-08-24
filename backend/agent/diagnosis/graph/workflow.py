# coding: utf-8

from langgraph.graph import END, StateGraph, START
from agent.diagnosis.graph.state import PlanExecute
from agent.diagnosis.graph.nodes import planFunc, execute, replan
from agent.diagnosis.graph.edges import should_end

def build_graph(llm, retriever):
    workflow = StateGraph(PlanExecute)

    # Nodes
    workflow.add_node("planer", planFunc(llm, retriever))
    workflow.add_node("execute", execute)
    workflow.add_node("replan", replan)

    # Edges
    workflow.add_edge(START, "planer")
    workflow.add_edge("planer", "execute")
    workflow.add_edge("execute", "replan")
    workflow.add_conditional_edges("replan", should_end)

    # Compile
    return workflow.compile()
