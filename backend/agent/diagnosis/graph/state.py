# coding: utf-8

from typing import TypedDict, Annotated, List, Tuple

def get_counter(a, b):
    print(a, b)
    return a

class PlanExecute(TypedDict):
    issue: str
    plan: str
    executed_plans: str
    number: int
    end: bool
