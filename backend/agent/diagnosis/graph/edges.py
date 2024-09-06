# coding: utf-8

import logging
from typing import Literal

logger = logging.getLogger(__name__)

def should_end(state) -> Literal["execute", "__end__"]:
    logger.debug(state["termination"])
    if state["termination"] is True:
        return "__end__"
    else:
        return "execute"
