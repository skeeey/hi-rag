# coding: utf-8

import logging, time
from llama_index.core import VectorStoreIndex, Settings
from llms.models import get_models
from loaders.load_data import load_all_data
from common.settings import *

logging.basicConfig(level=logging.INFO)

load_all_data()

if INDEX_DIR == None:
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
index.storage_context.persist(persist_dir=INDEX_DIR)
logging.info("index is built, time used %.3fs", (time.time() - start_time))
