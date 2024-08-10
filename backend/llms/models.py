# coding: utf-8

import logging
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from common.settings import *

logger = logging.getLogger(__name__)

def get_llm_model():
    logger.info("mode %s is used with %s", LLM_MODEL_NAME, LLM_MODEL_PROVIDER)

    if LLM_MODEL_PROVIDER == 'groq':
        if GROQ_TOKEN == None:
            raise ValueError("`GROQ_TOKEN` is required")
        
        return Groq(model=LLM_MODEL_NAME, api_key=GROQ_TOKEN)
    elif LLM_MODEL_PROVIDER == 'ollama':
        return Ollama(model=LLM_MODEL_NAME, request_timeout=600.0)

def get_embedding_model():
    logger.info("embedding mode %s is used with %s", EMBEDDING_MODEL_NAME, EMBEDDING_MODEL_PROVIDER)

    if EMBEDDING_MODEL_PROVIDER == 'huggingface':
        return HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)
    elif EMBEDDING_MODEL_PROVIDER == 'ollama':
        return OllamaEmbedding(model_name=EMBEDDING_MODEL_NAME)

def get_models():
    return get_llm_model(), get_embedding_model()
