# coding: utf-8

import os
import logging
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat.engine import ChatEngine

logging.basicConfig(level=logging.INFO)

class Message(BaseModel):
    id: str
    content: str

# Create a chat engine
index_dir=os.path.join(os.getcwd(), "backend", "data", "index")
embed_model = OllamaEmbedding("llama3:8b")
llm = Ollama(model="llama3:8b", request_timeout=600.0)
Settings.llm = llm
Settings.embed_model = embed_model

chatEngine=ChatEngine(index_dir, llm, verbose=False)

# Create a http server
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(msg: Message):
    if len(msg.content) == 0:
        return HTTPException(status_code=422, detail="the msg content is required")
    
    try:
        chatResponse=chatEngine.chat(msg.content.strip())
        logging.debug("answer question[%s] %s", msg.id, chatResponse.response)
        return Message(id=msg.id, content=chatResponse.response)
    except Exception as e:
        logging.error('Error at chat', exc_info=e)
        return HTTPException(status_code=500, detail="failed to answer the question")
