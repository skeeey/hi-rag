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
POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
POSTGRES_DATABASE_TABLE = os.getenv("POSTGRES_DATABASE_TABLE", default="hi_rag")

CHROMA_DIR = os.getenv("CHROMA_DIR")

# model settings
LLM_MODEL = os.getenv("LLM_MODEL", default="llama3.1")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")
MISTRAL_TOKEN = os.getenv("MISTRAL_TOKEN")

# index settings
INDEX_DIR = os.getenv("INDEX_DIR")

# local data settings
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR")

# jira data settings
JIRA_SEVER = os.getenv("JIRA_SEVER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
