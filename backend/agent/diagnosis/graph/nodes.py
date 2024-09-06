# coding: utf-8

import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from agent.diagnosis.graph.state import new_status
from agent.diagnosis.tools.runner import (
    to_step_dict, is_executable_step, has_real_cause, print_step, run_cmds, get_question
    )
from agent.diagnosis.tools.rag import query_with_retriever
from prompt.templates import GENERATE_PLAN_PROMPT, GENERATE_NEXT_STEP_PROMPT

logger = logging.getLogger(__name__)

def plan_func(llm, retriever):
    def plan(state):
        logger.info("---[DIAGNOSIS] CALL PLAN---")
        issue = state["issue"]
        print("Planing the diagnosis flow ...")
        # init a plan
        plan = query_with_retriever(llm, retriever, GENERATE_PLAN_PROMPT, issue)
        return new_status(issue=issue, plan=plan)
    return plan

def replan_func(llm, retriever):
    def replan(state):
        logger.info("---[DIAGNOSIS] CALL REPLAN---")
        if state["termination"] is True:
            return new_status(termination=True)

        root_cause = state["root_cause"]
        print(f"Root cause: {root_cause}")
        return new_status(termination=True)
    return replan

def execute_func(llm):
    def execute(state):
        logger.info("---[DIAGNOSIS] CALL Execute---")

        issue = state["issue"]
        plan = state["plan"]
        history = state["execution_history"]

        print(plan)
        confirmation = input("Do you want the AI assistant to diagnose the issue with this plan? (y/N) ")
        if confirmation.strip() == "y":
            while True:
                prompt = PromptTemplate(
                    template=GENERATE_NEXT_STEP_PROMPT,
                    input_variables=["issue", "plan", "execution_history"])
                llm_chain = (prompt | llm | StrOutputParser())
                llm_step = llm_chain.invoke({"issue": issue, "plan": plan, "execution_history": history})
                #logger.info(llm_step)

                step = to_step_dict(llm_step)

                if has_real_cause(step) is True:
                    print(step)
                    return new_status(issue=issue, plan=plan, root_cause=step["root_cause"], execution_history=history)

                print_step(step)
                step_confirmation = input("Do you want the AI assistant to execute this step? (y/N) ")
                if step_confirmation.strip() != "y":
                    return new_status(termination=True)

                if is_executable_step(step) is False:
                    # TODO the step is not executable, we may end here??
                    return new_status(termination=True)

                executed_step = run_cmds(step)
                history = history + executed_step

        return new_status(termination=True)
    return execute