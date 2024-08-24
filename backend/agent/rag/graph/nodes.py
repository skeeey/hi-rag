# coding: utf-8

import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from prompt.templates import GENERATE_PROMPT

logger = logging.getLogger(__name__)

def agentFunc(llm, tools):
    def agent(state):
        logger.info("---[RAG] CALL AGENT---")
        logger.info(state)
        messages = state["messages"]
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    return agent


def rewriteFunc(llm):
    def rewrite(state):
        logger.info("---[RAG] TRANSFORM QUERY---")
        messages = state["messages"]
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
        Look at the input and try to reason about the underlying semantic intent / meaning. \n 
        Here is the initial question:
        \n ------- \n
        {question} 
        \n ------- \n
        Formulate an improved question: """,
            )
        ]

        response = llm.invoke(msg)
        return {"messages": [response]}
    return rewrite


def generateFunc(llm):
    def generate(state):
        logger.info("---[RAG] GENERATE---")
        messages = state["messages"]
        question = messages[0].content
        last_message = messages[-1]

        question = messages[0].content
        docs = last_message.content
        rag_custom_prompt = PromptTemplate(template=GENERATE_PROMPT, input_variables=["context", "question"])

        # Chain
        rag_chain = rag_custom_prompt | llm | StrOutputParser()

        # Run
        response = rag_chain.invoke({"context": docs, "question": question})
        return {"messages": [response]}
    return generate
