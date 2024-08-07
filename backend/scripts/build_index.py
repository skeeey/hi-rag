# coding: utf-8

import os, sys, getopt

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file import PDFReader
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def get_args(argv):
    model="llama3.1"
    data_dir=os.path.join(os.getcwd(), "backend", "data", "example", "doc")
    index_dir=os.path.join(os.getcwd(), "backend", "data", "example", "index")

    try:
        opts, _ = getopt.getopt(argv, "hm:i:o:",["model=","data-dir=","index-dir="])
    except getopt.GetoptError:
        print("build_index.py -m <ollama model> -i <data dir> -o <index dir>")
        sys.exit(1)
    
    if len(opts) == 0:
        return model, data_dir, index_dir

    for opt, arg in opts:
        if opt == '-h':
            print("build_index.py -m <ollama model> -i <data dir> -o <index dir>")
            sys.exit()
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-i", "--data-dir"):
            data_dir = arg
        elif opt in ("-o", "--index-dir"):
            index_dir = arg
    return model, data_dir, index_dir

if __name__ == "__main__":
    model, data_dir, index_dir=get_args(sys.argv[1:])
    print("model: %s, data: %s, index: %s" % (model, data_dir, index_dir))

    llm = Ollama(model=model, request_timeout=120.0)
    #embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embed_model = OllamaEmbedding(model)

    # Set model
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    # Load Data
    # TODO load data from different sources
    print("loading data ...")
    docs = SimpleDirectoryReader(data_dir, file_extractor={".pdf": PDFReader()}).load_data()
    
    # Build index
    print("build index ...")
    index = VectorStoreIndex.from_documents(docs)
    # TODO try to introduce a database
    index.storage_context.persist(persist_dir=index_dir)
