# coding: utf-8

import logging
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader
from llama_index.readers.jira import JiraReader
from common.settings import *

# TODO support more loader with different data source

def load_local_data():
    if LOCAL_DATA_DIR == None:
        logging.info("`LOCAL_DATA_DIR` not set, ignore")
        return []
    logging.info("loading local data from %s ...", LOCAL_DATA_DIR)
    return SimpleDirectoryReader(LOCAL_DATA_DIR, file_extractor={".pdf": PDFReader()}).load_data()

def load_jira_data():
    if JIRA_SEVER == None or JIRA_TOKEN == None:
        logging.info("JIRA configurations not set, ignore")
        return []
    # TODO support configure this
    query = "project = ACM AND issuetype = Bug AND status = Closed AND component = \"Server Foundation\" ORDER BY updated DESC"
    logging.info("loading data from jira %s with query %s ...", JIRA_SEVER, query)
    return JiraReader(PATauth={"server_url": JIRA_SEVER, "api_token": JIRA_TOKEN}).load_data(query=query)

def load_all_data(loaders=[load_local_data, load_jira_data]):
    documents = []
    for loader in loaders:
        documents.extend(loader())
    return documents
