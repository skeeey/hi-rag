# coding: utf-8

import pprint
import logging
from agent.rag.tools.query import query_with_retriever
from prompt.templates import GENERATE_PROMPT

logger = logging.getLogger(__name__)

def planFunc(llm, retriever):
    def plan(state):
        logger.info("---[DIAGNOSIS] CALL PLAN---")
        logger.info(state)
        answer = query_with_retriever(llm, retriever, GENERATE_PROMPT, state["issue"])
        logger.info("---[DIAGNOSIS] OUTPUT---")
        logger.info(answer)
        logger.info("---[DIAGNOSIS] OUTPUT---")
        return {"plan": answer}
    return plan

def replan(state):
    logger.info("---[DIAGNOSIS] CALL REPLAN---")
    if state["number"] == 5:
        return {"end": True}

    return {"number": state["number"]} 

def execute(state):
    logger.info("---[DIAGNOSIS] CALL Execute---")
    answer = input("Do you want to continue? (Y/N) ")
    if answer.strip() == "y" or answer.strip() == "Y":
        number = state["number"]
        number = number + 1
        return {"number": number, "end": False} 

    return {"end": True}