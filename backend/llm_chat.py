# coding: utf-8

import os, cmd, logging

from llama_index.core import Settings

import settings
from llms.models import get_models
from chat.engine import ChatEngine

logging.basicConfig(level=logging.INFO)

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
    llm, embed_model = get_models()
    Settings.llm = llm
    Settings.embed_model = embed_model
    LLMChat(ChatEngine(os.getenv(settings.INDEX_DIR), llm)).cmdloop()
