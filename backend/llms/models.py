# coding: utf-8

import os, logging

from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding

import settings

def get_llm_model():
    model_provider = os.getenv(settings.LLM_MODEL_PROVIDER, default=settings.DEFAULT_LLM_MODEL_PROVIDER)
    model_name = os.getenv(settings.LLM_MODEL_NAME, default=settings.DEFAULT_LLM_MODEL_NAME)
    logging.info("mode %s is used with %s", model_name, model_provider)
    if model_provider == 'groq':
        return Groq(model=model_name)
    elif model_provider == 'ollama':
        return Ollama(model=model_name, request_timeout=600.0)

def get_embedding_model():
    model_provider = os.getenv(settings.EMBEDDING_MODEL_PROVIDER, default=settings.DEFAULT_EMBEDDING_MODEL_PROVIDER)
    model_name = os.getenv(settings.EMBEDDING_MODEL_NAME, default=settings.DEFAULT_EMBEDDING_MODEL_NAME)
    logging.info("embedding mode %s is used with %s", model_name, model_provider)
    if model_provider == 'huggingface':
        return HuggingFaceEmbedding(model_name=model_name)
    elif model_provider == 'ollama':
        return OllamaEmbedding(model_name=model_name)

def get_models():
    return get_llm_model(), get_embedding_model()
