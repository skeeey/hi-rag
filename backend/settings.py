# coding: utf-8

import os

from dotenv import load_dotenv

load_dotenv()

# model settings
LLM_MODEL_PROVIDER = "LLM_MODEL_PROVIDER"
LLM_MODEL_NAME = "LLM_MODEL_NAME"

DEFAULT_LLM_MODEL_PROVIDER = "ollama"
DEFAULT_LLM_MODEL_NAME = "llama3.1"

# embedding model settings
EMBEDDING_MODEL_PROVIDER = "EMBEDDING_MODEL_PROVIDER"
EMBEDDING_MODEL_NAME = "EMBEDDING_MODEL_NAME"

DEFAULT_EMBEDDING_MODEL_PROVIDER = "ollama"
DEFAULT_EMBEDDING_MODEL_NAME = "llama3.1"

# index settings
INDEX_DIR = "INDEX_DIR"

# local data settings
LOCAL_DATA_DIR = "LOCAL_DATA_DIR"

# jira data settings
JIRA_SEVER = "JIRA_SEVER"
JIRA_TOKEN = "JIRA_TOKEN"
