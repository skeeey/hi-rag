# coding: utf-8

import logging
import pprint
from IPython.display import Image
from agent.diagnosis.builder import build_diagnosis_agent
from agent.rag.builder import build_rag_agent
from agent.rag.loader.markdown import load_doc
from agent.rag.tools.query import query_with_retriever
from agent.rag.tools.retriever import build_retriever
from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, LOCAL_DATA_DIR, GROQ_TOKEN
from llms.langchain.providers import groq
from prompt.templates import GENERATE_PROMPT

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

def print_flow(graph):
    image = Image(graph.get_graph(xray=True).draw_mermaid_png())
    with open("agent-flow.png", "wb") as png:
        png.write(image.data)

def run_rag_agent(question):
    graph = build_rag_agent(doc_dir=LOCAL_DATA_DIR)
    inputs = {
        "messages": [("user", question)]
    }
    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")

def run_rag_query_tool(question):
    docs = load_doc(LOCAL_DATA_DIR)
    retriever = build_retriever(docs)
    llm = groq(api_key=GROQ_TOKEN)
    output = query_with_retriever(llm, retriever, GENERATE_PROMPT, question)
    print(output)

def run_diagnosis_agent(question):
    graph = build_diagnosis_agent(doc_dir=LOCAL_DATA_DIR)
    graph.invoke({"issue": question}, config={"recursion_limit": 50})

if __name__ == "__main__":
    question = "My cluster named cluster1 status is unknown in the ACM hub, how can I fix it?"
    run_diagnosis_agent(question)
