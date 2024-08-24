# coding: utf-8

"""
Build the index with the given data and save the index to a given chroma
"""

import logging
import time
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llms.models import get_embedding_model
from loaders.all import load_all_data
from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, CHROMA_DIR

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if CHROMA_DIR is None:
        raise ValueError("'CHROMA_DIR' is required")

    # Set embedding model
    Settings.embed_model = get_embedding_model()

    # Load Data
    docs = load_all_data()
    if len(docs) == 0:
        raise ValueError("no documents are provided")

    # Build index
    start_time = time.time()
    db = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = db.get_or_create_collection("hi-rag")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=StorageContext.from_defaults(vector_store=vector_store),
        show_progress=True,
    )
    logger.info("index is built, time used %.3fs", (time.time() - start_time))
