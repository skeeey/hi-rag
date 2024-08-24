# coding: utf-8

"""
Run a chat bot locally
"""

import cmd
import logging
from llama_index.core import Settings
from llms.models import get_models
from chat.engine import ChatEngine
from config.settings import (
    LOG_FORMAT,
    LOG_DATE_FORMAT,
    INDEX_DIR,
    CHROMA_DIR,
    POSTGRES_DATABASE_URL,
    POSTGRES_DATABASE_TABLE
    )

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)

class LLMChat(cmd.Cmd):
    """
    LLMChat (based on cmd) provides a line-oriented command interpreter
    """

    intro = (
        "Welcome to the chat shell. \n"
        "Using `m <Your message>` to send a message. \n"
        "Type help or ? to list commands.\n"
    )
    prompt = "(Chat🦙) "

    def __init__(self, engine:ChatEngine):
        super().__init__()
        self.engine = engine

    def do_m(self, message):
        """Send a question to the current conversation and get back the AI's response: m <Your message>"""
        resp = self.engine.chat(message.strip())
        print(f"\n\n{resp}")

    def do_bye(self, _):
        """Quits the chat."""
        print("Bye")
        raise SystemExit

if __name__ == "__main__":
    llm, embed_model = get_models()
    Settings.llm = llm
    Settings.embed_model = embed_model
    chat_engine = ChatEngine(
        local_index_dir=INDEX_DIR,
        chroma_dir=CHROMA_DIR,
        postgres_url=POSTGRES_DATABASE_URL,
        postgres_table=POSTGRES_DATABASE_TABLE,
        llm=llm,
        verbose=False,
    )
    LLMChat(chat_engine).cmdloop()
