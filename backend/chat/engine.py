# coding: utf-8

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from common.settings import CONTEXT_PROMPT

class ChatEngine:
    def __init__(self, indexDir, llm, verbose=True):
      # load index from local index dir
      index = load_index_from_storage(StorageContext.from_defaults(persist_dir=indexDir))
      self.chatEngine = CondensePlusContextChatEngine.from_defaults(
        retriever=VectorIndexRetriever(index=index, similarity_top_k=3),
        memory=ChatMemoryBuffer.from_defaults(token_limit=40960),
        llm=llm,
        context_prompt=CONTEXT_PROMPT,
        verbose=verbose,
      )

    def chat(self, question):
       response = self.chatEngine.chat(question)
       return response
