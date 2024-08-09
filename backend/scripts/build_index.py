# coding: utf-8

import logging, os, time

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PDFReader

import settings
from llms.models import get_models
from loaders.load_data import load_all_data

logging.basicConfig(level=logging.INFO)

index_dir = os.getenv(settings.INDEX_DIR)
if index_dir == None:
    raise ValueError("'INDEX_DIR' is required")

# Set model
llm, embed_model = get_models()
Settings.llm = llm
Settings.embed_model = embed_model

# Load Data
docs = load_all_data()

if len(docs) == 0:
    raise ValueError("no documents are provided")

# Build index
logging.info("build index ...")
start_time = time.time()
index = VectorStoreIndex.from_documents(docs)
# TODO support a database
index.storage_context.persist(persist_dir=index_dir)
logging.info("index is built, time used %.3fs", (time.time() - start_time))
