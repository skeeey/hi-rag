# coding: utf-8

import os, logging

from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader
from llama_index.readers.jira import JiraReader

import settings

# TODO support more loader with different data source

def load_local_data():
    data_dir=os.getenv(settings.LOCAL_DATA_DIR)
    if data_dir == None:
        logging.debug("no local data configuration, ignore")
        return []
    logging.info("loading data from %s ...", data_dir)
    return SimpleDirectoryReader(data_dir, file_extractor={".pdf": PDFReader()}).load_data()

def load_jira_data():
    server = os.getenv(os.getenv(settings.JIRA_SEVER))
    api_token = os.getenv(os.getenv(settings.JIRA_TOKEN))
    if server == None or api_token == None:
        logging.debug("no jira configuration, ignore")
        return []
    # TODO support configure this
    query = "project = ACM AND issuetype = Bug AND status = Closed AND component = \"Server Foundation\" ORDER BY updated DESC"
    logging.info("loading data from jira %s with query %s ...", server, query)
    reader=JiraReader(PATauth={ "server_url": server, "api_token": api_token })
    return reader.load_data(query=query)

def load_all_data():
    documents = load_local_data()
    documents.append(load_jira_data())
    return documents
