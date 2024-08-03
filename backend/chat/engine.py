# coding: utf-8

from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine

class ChatEngine:
    def __init__(self, indexDir, llm, verbose=True):
      # load index from local index dir
      index = load_index_from_storage(StorageContext.from_defaults(persist_dir=indexDir))
      retriever = VectorIndexRetriever(index=index, similarity_top_k=10)
      self.chatEngine = CondensePlusContextChatEngine.from_defaults(
        retriever,
        memory=ChatMemoryBuffer.from_defaults(token_limit=40960),
        llm=llm,
        # context_prompt=(
        #     "You are a Red Hat Advanced Cluster Management (aka ACM) expert, you are able to have normal interactions, as well as talk"
        #     " about the ACM."
        #     "Here are the relevant documents for the context:\n"
        #     "{context_str}"
        #     "\nInstruction: Use the previous chat history, or the context above, to interact and help the user."
        # ),
        verbose=verbose,
      )

    def chat(self, question):
       response = self.chatEngine.chat(question)
       return response
    
    def streamChat(self, question):
      streaming_resp = self.chatEngine.stream_chat(question)
      for token in streaming_resp.response_gen:
          print(token, end="")
      return ""
