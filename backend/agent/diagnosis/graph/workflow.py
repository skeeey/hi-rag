# coding: utf-8

from langgraph.graph import END, StateGraph, START
from agent.diagnosis.graph.state import StepExecute
from agent.diagnosis.graph.nodes import plan_func, execute_func, replan_func
from agent.diagnosis.graph.edges import should_end

def build_graph(llm, retriever):
    workflow = StateGraph(StepExecute)

    # Nodes
    workflow.add_node("planer", plan_func(llm, retriever))
    workflow.add_node("execute", execute_func(llm))
    workflow.add_node("replan", replan_func(llm, retriever))

    # Edges
    workflow.add_edge(START, "planer")
    workflow.add_edge("planer", "execute")
    workflow.add_edge("execute", "replan")
    workflow.add_conditional_edges("replan", should_end)

    # Compile
    return workflow.compile()
