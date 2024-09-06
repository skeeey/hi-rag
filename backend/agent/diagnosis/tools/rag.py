# coding: utf-8

import logging
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool

logger = logging.getLogger(__name__)

def query_with_retriever(llm, retriever, prompt_template, issue):
    prompt = PromptTemplate(template=prompt_template, input_variables=["issue", "context"])
    docs = retriever.invoke(issue)
    docs_txt = []
    for doc in docs:
        docs_txt.append(doc.page_content)
    llm_chain = (prompt | llm | StrOutputParser())
    return llm_chain.invoke({"issue": issue, "context": ("\n".join(docs_txt))})


def list_md_files(start_path, exclude_list):
    file_list = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not d == '.git']
        
        for f in files:
            if f.endswith('.md') and f not in exclude_list:
                file_list.append(os.path.join(root, f))

    return file_list

def load_doc(dir, exclude_list=None):
    if exclude_list is None:
        exclude_list = ["README.md", "SECURITY.md", "index.md"]

    files = list_md_files(dir, exclude_list)
    docs = []
    for md in files:
        logger.debug("load data from file: %s", md)
        loader = UnstructuredMarkdownLoader(md, mode="single", strategy="fast")
        docs.extend(loader.load())

    return docs

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
    return retriever

def build_retriever_tool(docs):
    retriever = build_retriever(docs)
    return create_retriever_tool(
        retriever,
        "retrieve_docs",
        "Search and return information about ACM troubleshooting document on LLM agents.",
    )