# coding: utf-8


"""
Provide a chat engine with the given LLM and index
"""

import logging
import chromadb
from sqlalchemy import make_url
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from prompt.templates import CHAT_CONTEXT_PROMPT

logger = logging.getLogger(__name__)

class ChatEngine:
    """
    ChatEngine is CondensePlusContextChatEngine
    """

    def __init__(self, local_index_dir, chroma_dir, postgres_url, postgres_table, llm, verbose=True):
        index = None

        if local_index_dir:
            logger.info("load index from local dir: %s", local_index_dir)
            index = load_index_from_storage(StorageContext.from_defaults(persist_dir=local_index_dir))

        if chroma_dir:
            db = chromadb.PersistentClient(path=chroma_dir)
            chroma_collection = db.get_collection("hi-rag")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        if postgres_url:
            url = make_url(postgres_url)
            logger.info("load index from Postgres: %s.%s", url.database, postgres_table)
            vector_store = PGVectorStore.from_params(
                database=url.database,
                host=url.host,
                password=url.password,
                port=url.port,
                user=url.username,
                table_name=postgres_table,
                embed_dim=384,
                hnsw_kwargs={
                      "hnsw_m": 16, 
                      "hnsw_ef_construction": 64,
                      "hnsw_ef_search": 40,
                      "hnsw_dist_method": "vector_cosine_ops",
                },
            )
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        if index is None:
            raise ValueError("index is required")

        self.chat_engine = CondensePlusContextChatEngine.from_defaults(
           retriever=VectorIndexRetriever(index=index, similarity_top_k=10),
           memory=ChatMemoryBuffer.from_defaults(token_limit=40960),
           llm=llm,
           context_prompt=CHAT_CONTEXT_PROMPT,
           verbose=verbose,
        )

    def chat(self, question):
        response = self.chat_engine.chat(question)
        return response
