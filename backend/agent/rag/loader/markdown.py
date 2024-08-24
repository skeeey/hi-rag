# coding: utf-8

# import nltk
# nltk.download('punkt')
# nltk.download('punkt_tab')
import logging
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader

logger = logging.getLogger(__name__)

def list_md_files(start_path, exclude_list):
    file_list = []
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not d == '.git']
        
        for f in files:
            if f.endswith('.md') and f not in exclude_list:
                file_list.append(os.path.join(root, f))

    return file_list

def load_doc(dir, exclude_list=None):
    if exclude_list is None:
        exclude_list = ["README.md", "SECURITY.md", "index.md"]

    files = list_md_files(dir, exclude_list)
    docs = []
    for md in files:
        logger.debug("load data from file: %s", md)
        loader = UnstructuredMarkdownLoader(md, mode="single", strategy="fast")
        docs.extend(loader.load())

    return docs
