# coding: utf-8

from typing import TypedDict

class StepExecute(TypedDict):
    issue: str
    root_cause: str
    plan: str
    execution_history: str
    termination: bool

def new_status(issue="", root_cause="", plan="", execution_history="", termination=False):
    return {
        "issue": issue,
        "plan": plan,
        "root_cause": root_cause,
        "execution_history": execution_history,
        "termination": termination,
    }
