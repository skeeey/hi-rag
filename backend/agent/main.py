# coding: utf-8

import logging
from IPython.display import Image
from agent.diagnosis.builder import build_diagnosis_agent
from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, LOCAL_DATA_DIR, GROQ_TOKEN

logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

def print_flow(graph):
    image = Image(graph.get_graph(xray=True).draw_mermaid_png())
    with open("agent-flow.png", "wb") as png:
        png.write(image.data)

def run_diagnosis_agent(question):
    graph = build_diagnosis_agent(doc_dir=LOCAL_DATA_DIR)
    graph.invoke({"issue": question}, config={"recursion_limit": 50})

if __name__ == "__main__":
    question = "My cluster named cluster1 status is unknown in the ACM hub, how can I fix it?"
    print(f"Issue: {question}")
    run_diagnosis_agent(question)
