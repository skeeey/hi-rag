# coding: utf-8

import logging, time
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader, MarkdownReader
from llama_index.readers.jira import JiraReader
from llms.models import get_embedding_model
from common.settings import *

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

# TODO support more loader with different data source

def load_local_data():
    if LOCAL_DATA_DIR == None:
        logger.warning("`LOCAL_DATA_DIR` not set, ignore")
        return []
    logger.info("loading local data from %s ...", LOCAL_DATA_DIR)
    file_extractor = {
        ".pdf": PDFReader(),
        ".md": MarkdownReader(),
        ".adoc": MarkdownReader(),
    }
    return SimpleDirectoryReader(LOCAL_DATA_DIR, file_extractor=file_extractor).load_data()

def load_jira_data():
    if JIRA_SEVER == None or JIRA_TOKEN == None:
        logger.warning("JIRA configurations not set, ignore")
        return []
    # TODO support configure this
    query = "project = ACM AND issuetype = Bug AND status = Closed AND component = \"Server Foundation\" ORDER BY updated DESC"
    logger.info("loading data from jira %s with query %s ...", JIRA_SEVER, query)
    return JiraReader(PATauth={"server_url": JIRA_SEVER, "api_token": JIRA_TOKEN}).load_data(query=query)

def load_all_data(loaders=[load_local_data, load_jira_data]):
    documents = []
    for loader in loaders:
        documents.extend(loader())
    return documents

if __name__ == '__main__':
    if INDEX_DIR == None:
        raise ValueError("'INDEX_DIR' is required")

    # Set model
    embed_model = get_embedding_model()
    #Settings.llm = llm
    Settings.embed_model = embed_model

    # Load Data
    docs = load_all_data()
    if len(docs) == 0:
        raise ValueError("no documents are provided")

    # Build index
    logger.info("build index ...")
    start_time = time.time()
    index = VectorStoreIndex.from_documents(docs, show_progress=True)
    # TODO support a database
    index.storage_context.persist(persist_dir=INDEX_DIR)
    logger.info("index is built, time used %.3fs", (time.time() - start_time))
