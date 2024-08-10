# coding: utf-8

import cmd, logging
from llama_index.core import Settings
from llms.models import get_models
from chat.engine import ChatEngine
from common.settings import *

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

class LLMChat(cmd.Cmd):
    intro = (
        "Welcome to the chat shell. \n"
        "Using `m <Your message>` to send a message. \n"
        "Type help or ? to list commands.\n"
    )
    prompt = '(Chat🦙) '

    def __init__(self, engine:ChatEngine):
        super().__init__()
        self.engine = engine

    def do_m(self, message):
        """Send a question to the current conversation and get back the AI's response: m <Your message>"""
        print("\n\n%s"%self.engine.chat(message.strip()))

    def do_bye(self, args):
        """Quits the chat."""
        print('Bye')
        raise SystemExit

if __name__ == '__main__':
    llm, embed_model = get_models()
    Settings.llm = llm
    Settings.embed_model = embed_model
    LLMChat(ChatEngine(INDEX_DIR, llm, verbose=False)).cmdloop()
