# coding: utf-8

import logging
from agent.diagnosis.graph.workflow import build_graph
from agent.diagnosis.tools.rag import load_doc
from agent.diagnosis.tools.rag import build_retriever
from llms.langchain.providers import mistral, groq
from config.settings import MISTRAL_TOKEN, GROQ_TOKEN

logger = logging.getLogger(__name__)

def build_diagnosis_agent(doc_dir):
    logger.info("Load data ...")
    print("Read the runbooks from: %s"%(doc_dir))
    docs = load_doc(doc_dir)

    logger.info("Build retriever ...")
    retriever = build_retriever(docs)

    llm = groq(api_key=GROQ_TOKEN)

    return build_graph(llm, retriever)
