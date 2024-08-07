# coding: utf-8

import os, cmd, getopt, sys

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from chat.engine import ChatEngine

def get_args(argv):
    model="llama3.1"
    index_dir=os.path.join(os.getcwd(), "data", "example", "index")

    try:
        opts, _ = getopt.getopt(argv, "hm:i:",["model=","index-dir="])
    except getopt.GetoptError:
        print("llm_chat.py -m <ollama model> -i <data dir>")
        sys.exit(1)
    
    if len(opts) == 0:
        return model, index_dir

    for opt, arg in opts:
        if opt == '-h':
            print("llm_chat.py -m <ollama model> -i <data dir>")
            sys.exit()
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-o", "--index-dir"):
            index_dir = arg
    return model, index_dir


class LLMChat(cmd.Cmd):
    intro = 'Welcome to the chat shell.   Type help or ? to list commands.\n'
    prompt = '(Chat🦙) '

    def __init__(self, engine:ChatEngine):
        super().__init__()
        self.engine = engine

    def do_q(self, message):
        "Send a question to the current conversation and get back the AI's response: q <Your message>"
        print(self.engine.chat(message.strip()))

    def do_bye(self, args):
        "Quits the chat."
        print('Bye')
        raise SystemExit

if __name__ == '__main__':
    model, index_dir=get_args(sys.argv[1:])
    print("model: %s, index: %s" % (model, index_dir))

    embed_model = OllamaEmbedding(model)
    llm = Ollama(model=model, request_timeout=600.0)
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    LLMChat(ChatEngine(index_dir, llm)).cmdloop()
