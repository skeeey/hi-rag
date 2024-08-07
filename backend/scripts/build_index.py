# coding: utf-8

import os, sys, getopt

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PDFReader
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding

script_name="build_index"

def get_dirs(argv):
    data_dir=os.path.join(os.getcwd(), "backend", "data", "example", "doc")
    index_dir=os.path.join(os.getcwd(), "backend", "data", "example", "index")

    try:
        opts, _ = getopt.getopt(argv, "hi:o:",["data-dir=","index-dir="])
    except getopt.GetoptError:
        print("%s.py -i <data dir> -o <index dir>" % script_name)
        sys.exit(1)
    
    if len(opts) == 0:
        print("use example data")
        return data_dir, index_dir

    for opt, arg in opts:
        if opt == '-h':
            print("%s.py -i <data dir> -o <index dir>" % script_name)
            sys.exit()
        elif opt in ("-i", "--data-dir"):
            data_dir = arg
        elif opt in ("-o", "--index-dir"):
            index_dir = arg

if __name__ == "__main__":
    data_dir, index_dir=get_dirs(sys.argv[1:])

    llm = Ollama(model="llama3:8b", request_timeout=120.0)
    #embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embed_model = OllamaEmbedding("llama3:8b")

    # Set model
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    # Load Data
    # TODO load data from different sources
    docs = SimpleDirectoryReader(data_dir, file_extractor={".pdf": PDFReader()}).load_data()
    
    # Build index
    index = VectorStoreIndex.from_documents(docs)
    # TODO try to introduce a database
    index.storage_context.persist(persist_dir=index_dir)
