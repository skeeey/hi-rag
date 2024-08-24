# coding: utf-8

"""
Run a chat sever with FastAPI
"""

import logging
from llama_index.core import Settings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llms.models import get_models
from chat.engine import ChatEngine
from config.settings import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    INDEX_DIR,
    CHROMA_DIR,
    POSTGRES_DATABASE_URL,
    POSTGRES_DATABASE_TABLE,
    )

# setting logger
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

class Message(BaseModel):
    id: str
    content: str

# Create a chat engine
llm, embed_model = get_models()
Settings.llm = llm
Settings.embed_model = embed_model
chat_engine = ChatEngine(
    local_index_dir=INDEX_DIR,
    chroma_dir=CHROMA_DIR,
    postgres_url=POSTGRES_DATABASE_URL,
    postgres_table=POSTGRES_DATABASE_TABLE,
    llm=llm,
    verbose=False)

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

@app.get("/")
async def root():
    return {"message": "Hi, RAG"}

@app.post("/chat")
async def chat(msg: Message):
    if len(msg.content) == 0:
        return HTTPException(status_code=422, detail="the msg content is required")
    try:
        chat_response=chat_engine.chat(msg.content.strip())
        return Message(id=msg.id, content=chat_response.response)
    except Exception as e:
        logger.error("Error at chat", exc_info=e)
        return HTTPException(status_code=500, detail="failed to answer the question")
