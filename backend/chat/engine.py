# coding: utf-8


"""
Provide a chat engine with the given LLM and index
"""

import logging
from sqlalchemy import make_url

from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from config.settings import CONTEXT_PROMPT

logger = logging.getLogger(__name__)

class ChatEngine:
    """
    ChatEngine is CondensePlusContextChatEngine
    """

    def __init__(self, index_dir, database_url, database_table, llm, verbose=True):
        index = None

        if index_dir:
            logger.info("load index from %s", index_dir)
            index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_dir))

        if database_url:
            url = make_url(database_url)
            logger.info("load index from database %s.%s", url.database, database_table)
            vector_store = PGVectorStore.from_params(
                database=url.database,
                host=url.host,
                password=url.password,
                port=url.port,
                user=url.username,
                table_name=database_table,
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
           context_prompt=CONTEXT_PROMPT,
           verbose=verbose)

    def chat(self, question):
        response = self.chat_engine.chat(question)
        return response
