# coding: utf-8

"""
Loaders to load data from different data sources
"""

import logging
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader, MarkdownReader
from readers.jira import JiraReader
from config.settings import LOCAL_DATA_DIR, JIRA_SEVER, JIRA_TOKEN

logger = logging.getLogger(__name__)

# TODO support more loader with different data source

def load_local_data():
    if LOCAL_DATA_DIR is None:
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
    if JIRA_SEVER is None or JIRA_TOKEN is None:
        logger.warning("JIRA configurations not set, ignore")
        return []
    # TODO support configure this
    query = "project = ACM AND issuetype = Bug AND status = Closed AND component = \"Server Foundation\""
    query += " ORDER BY updated DESC"
    logger.info("loading data from jira %s with query %s ...", JIRA_SEVER, query)
    return JiraReader(pat_auth={"server_url": JIRA_SEVER, "api_token": JIRA_TOKEN}).load_data(query=query)

def load_all_data(loaders=None):
    if loaders is None:
        loaders = [load_local_data, load_jira_data]

    documents = []
    for loader in loaders:
        documents.extend(loader())
    return documents
