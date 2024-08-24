# coding: utf-8

import logging
from typing import Literal
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from prompt.templates import GRADE_PROMPT

logger = logging.getLogger(__name__)

def gradeFunc(llm):
    def grade_documents(state) -> Literal["generate", "rewrite"]:
        logger.info("---[RAG] CHECK RELEVANCE---")

        # Data model
        class grade(BaseModel):
            """Binary score for relevance check."""
            binary_score: str = Field(description="Relevance score 'yes' or 'no'")

        # LLM with tool and validation
        llm_with_tool = llm.with_structured_output(grade)

        # Prompt
        prompt = PromptTemplate(template=GRADE_PROMPT, input_variables=["context", "question"])

        # Chain
        chain = prompt | llm_with_tool

        messages = state["messages"]
        last_message = messages[-1]

        question = messages[0].content
        docs = last_message.content

        scored_result = chain.invoke({"question": question, "context": docs})

        score = scored_result.binary_score

        logger.info("---[RAG] RELEVANCE SCORE---")
        logger.info(score)
        logger.info("---[RAG] RELEVANCE SCORE---")

        if score == "yes":
            return "generate"
        else:
            return "rewrite"
    return grade_documents
