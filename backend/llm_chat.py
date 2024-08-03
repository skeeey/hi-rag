# coding: utf-8

import os
import cmd

from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from chat.engine import ChatEngine

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
    index_dir=os.path.join(os.getcwd(), "backend", "data", "example", "index")
    embed_model = OllamaEmbedding("llama3:8b")
    llm = Ollama(model="llama3:8b", request_timeout=600.0)
    Settings.llm = llm
    Settings.embed_model = embed_model
    
    LLMChat(ChatEngine(index_dir, llm)).cmdloop()
