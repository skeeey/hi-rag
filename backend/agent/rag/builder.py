# coding: utf-8

import logging
from agent.rag.loader.markdown import load_doc
from agent.rag.tools.retriever import build_retriever
from agent.rag.graph.workflow import build_graph
from llms.langchain.providers import mistral
from config.settings import MISTRAL_TOKEN

logger = logging.getLogger(__name__)

def build_rag_agent(doc_dir):
    logger.info("Load data ...")
    docs = load_doc(doc_dir)

    logger.info("Build retriever ...")
    retriever = build_retriever(docs)

    logger.info("Build graph ...")
    llm = mistral(api_key=MISTRAL_TOKEN)
    return build_graph(llm, [retriever])
