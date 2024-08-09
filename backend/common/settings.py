# coding: utf-8

import os
from dotenv import load_dotenv

load_dotenv()

# model settings
LLM_MODEL_PROVIDER = os.getenv("LLM_MODEL_PROVIDER", default="ollama")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", default="llama3.1")

# embedding model settings
EMBEDDING_MODEL_PROVIDER = os.getenv("EMBEDDING_MODEL_PROVIDER", default="huggingface")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", default="BAAI/bge-small-en-v1.5")

# index settings
INDEX_DIR = os.getenv("INDEX_DIR")

# local data settings
LOCAL_DATA_DIR = os.getenv("LOCAL_DATA_DIR")

# jira data settings
JIRA_SEVER = os.getenv("JIRA_SEVER")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
