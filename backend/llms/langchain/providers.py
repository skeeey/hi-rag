# coding: utf-8

from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI

def groq(api_key, model="llama-3.1-70b-versatile", temperature=0, timeout=120):
    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=temperature,
        timeout=timeout,
    )

def mistral(api_key, model="mistral-large-latest", temperature=0, timeout=120):
    return ChatMistralAI(
        model=model,
        api_key=api_key,
        temperature=temperature,
        timeout=timeout,
    )
