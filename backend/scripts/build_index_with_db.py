# coding: utf-8

"""
Build the index with the given data and save the index to a given database
"""

import logging
import time
from sqlalchemy import make_url
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.postgres import PGVectorStore
from llms.models import get_embedding_model
from loaders.all import load_all_data
from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, DATABASE_URL, DATABASE_TABLE

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if DATABASE_URL is None:
        raise ValueError("'DATABASE_URL' is required")

    # Set embedding model
    Settings.embed_model = get_embedding_model()

    # Load Data
    docs = load_all_data()
    if len(docs) == 0:
        raise ValueError("no documents are provided")

    # Build index
    start_time = time.time()
    url = make_url(DATABASE_URL)
    logger.info("build index to database %s ...", url.database)

    vector_store = PGVectorStore.from_params(
        database=url.database,
        host=url.host,
        password=url.password,
        port=url.port,
        user=url.username,
        table_name=DATABASE_TABLE,
        embed_dim=384,  # BAAI/bge-small-en-v1.5 dimension
        # HNSW (Hierarchical Navigable Small World)
        #  - hnsw_m: This parameter refers to the maximum number of bidirectional links created for
        #       every new element during the construction of the graph.
        #  - hnsw_ef_construction: This parameter is used during the index building phase.
        #       Higher efConstruction values lead to a higher quality of the graph and, consequently,
        #       more accurate search results. However, it also means the index building process will
        #       take more time.
        #  - hnsw_ef_search: This parameter is used during the search phase. Like efConstruction, a
        #       larger efSearch value results in more accurate search results at the cost of increased
        #       search time. This value should be equal or larger than k (the number of nearest neighbors
        #       you want to return)
        hnsw_kwargs={
            "hnsw_m": 16, 
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops",
        },
    )
    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=StorageContext.from_defaults(vector_store=vector_store),
        # need more test, refer to
        # https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
        #transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=200)],
        show_progress=True,
        )
    logger.info("index is built, time used %.3fs", (time.time() - start_time))
