# coding: utf-8

"""
Build the index with the given data and save the index to the local file system
"""

import logging
import time
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llms.models import get_embedding_model
from loaders.all import load_all_data
from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, INDEX_DIR

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if INDEX_DIR is None:
        raise ValueError("'INDEX_DIR' is required")

    # Set embedding model
    Settings.embed_model = get_embedding_model()

    # Load Data
    docs = load_all_data()
    if len(docs) == 0:
        raise ValueError("no documents are provided")

    # Build index
    logger.info("build index ...")
    start_time = time.time()
    index = VectorStoreIndex.from_documents(
        docs,
        transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=10)],
        show_progress=True,
    )
    index.storage_context.persist(persist_dir=INDEX_DIR)
    logger.info("index is built, time used %.3fs", (time.time() - start_time))
