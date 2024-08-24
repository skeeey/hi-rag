# coding: utf-8

import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

logger = logging.getLogger(__name__)

def build_retriever(docs, embedding_model="BAAI/bge-small-en-v1.5", chunk_size=1024, chunk_overlap=50):
    embedding = HuggingFaceEmbeddings(model_name=embedding_model)

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    splitted_docs = text_splitter.split_documents(docs)

    # Add to vectorDB
    vector_store = Chroma.from_documents(
        documents=splitted_docs,
        collection_name="rag-chroma",
        embedding=embedding,
    )
    retriever = vector_store.as_retriever()

    return create_retriever_tool(
        retriever,
        "retrieve_docs",
        "Search and return information about ACM troubleshooting document on LLM agents.",
    )
