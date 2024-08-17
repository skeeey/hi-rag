# coding: utf-8

"""
Provide LLM models by different configurations
"""

import logging
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config.settings import GROQ_TOKEN, OPENAI_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

def get_llm_model():
    if GROQ_TOKEN and len(GROQ_TOKEN) != 0:
        logger.info("mode %s is used with groq", LLM_MODEL)
        return Groq(model=LLM_MODEL, api_key=GROQ_TOKEN)
    elif OPENAI_API_KEY and len(OPENAI_API_KEY) != 0:
        logger.info("mode %s is used with openai", LLM_MODEL)
        return OpenAI(temperature=0, model=LLM_MODEL, api_key=OPENAI_API_KEY)
    else:
        logger.info("mode %s is used with ollama", LLM_MODEL)
        return Ollama(model=LLM_MODEL, request_timeout=600.0)

def get_embedding_model():
    # TODO support more embedding model
    logger.info("embedding model: https://huggingface.co/BAAI/bge-small-en-v1.5")
    return HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

def get_models():
    return get_llm_model(), get_embedding_model()
