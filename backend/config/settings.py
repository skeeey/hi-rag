# coding: utf-8

"""
Settings to run build-index/chat bot/chat server
"""

import os
from dotenv import load_dotenv

load_dotenv()

# log settings
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(levelname)s: [%(asctime)s, %(module)s, line:%(lineno)d] %(message)s"

# DB settings
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_TABLE = os.getenv("DATABASE_TABLE", default="hi_rag")

# model settings
LLM_MODEL = os.getenv("LLM_MODEL", default="llama3.1")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")

# index settings
INDEX_DIR = os.getenv("INDEX_DIR")

# local data settings
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR")

# jira data settings
JIRA_SEVER = os.getenv("JIRA_SEVER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

# prompts
CONTEXT_PROMPT = """
The following is a friendly conversation between a user and an AI assistant aimed at solving
issues related to Red Hat Advanced Cluster Management (also known as ACM or RHACM).
The assistant is talkative and provides lots of specific details from its context.
If the assistant does not know the answer to a question, it truthfully says it does not know.

Here are the relevant documents for the context:

{context_str}

Please Note:
1. The "hub" for the given question always refers to the ACM Hub.
2. The "cluster" or "managed cluster" for the given question always refers to the ACM managed cluster.

Instruction: Based on the above documents, provide a detailed answer for the user question below.
If you need more details about the question, ask user to provide.
Answer "don't know" if not present in the document.
"""
