# coding: utf-8

import json
import time
from typing import TypedDict, Annotated, List
from operator import add

def mock_result(cmd):
    if "ManagedClusterConditionAvailable" in cmd:
        return "The ManagedClusterConditionAvailable is Unknown"

    if "ManagedClusterJoined" in cmd:
        return "The ManagedClusterJoined is True"

    if "ManagedClusterImportSucceeded" in cmd:
        return "The ManagedClusterImportSucceeded is True"
    
    if "get managedcluster cluster1" in cmd:
        return "The ManagedClusterConditionAvailable is Unknown\nThe ManagedClusterJoined is True\nThe ManagedClusterImportSucceeded is True\nThe ManagedClusterConditionClockSynced is True"
    
    if "get pod" in cmd:
        return "The pods are missing."
    
    if "get deployments" in cmd:
        return "The deployments are missing."
    
    if "get daemonsets" in cmd:
        return "The daemonsets are missing."
    
    if "get secrets" in cmd:
        return "The secrets are missing."

    return "The klusterlet is missing."

def to_step_dict(step):
    step = step.strip()
    begin = step.index("```json") + len("```json")
    end = step.index("```", begin + len("```json"))
    step = step[begin:end]
    # step = step.replace("```json", "", 1)
    # step = "".join(step.rsplit("```", 1))
    # print(step)
    return json.loads(step)

def has_real_cause(step):
    if len(step.get("root_cause", "")) != 0:
        return True
    return False

def is_executable_step(step):
    if len(step.get("hub_cmds", [])) != 0 or len(step.get("spoke_cmds", [])) != 0:
        return True
    return False

def get_question(content):
    question = content.strip()
    begin = question.index("```") + len("```")
    end = question.index("```", begin + len("```"))
    return question[begin:end]

def print_step(step):
    print("### %s" % (step["title"]))
    print("- Commands:")
    for cmd in step.get("hub_cmds", []):
        print(cmd.replace("oc", "oc --kubeconfig=hub.kubeconfig", 1))
    for cmd in step.get("spoke_cmds", []):
        print(cmd.replace("oc", "oc --kubeconfig=spoke.kubeconfig", 1))

def run_cmds(step):
    cmds_results=[]
    for cmd in step.get("hub_cmds", []):
        cmd_with_kubeconfig = cmd.replace("oc", "oc --kubeconfig=hub.kubeconfig", 1)
        result = mock_result(cmd)
        cmds_results.append(f"""- Command: {cmd}\n- Result: {result}""")
        print(cmd_with_kubeconfig)
        time.sleep(2)
        print(result)

    for cmd in step.get("spoke_cmds", []):
        cmd_with_kubeconfig = cmd.replace("oc", "oc --kubeconfig=spoke.kubeconfig", 1)
        result = mock_result(cmd)
        cmds_results.append(f"""- Command: {cmd}\n- Result: {result}""")
        print(cmd_with_kubeconfig)
        time.sleep(2)
        print(result)

    title = step["title"]
    results = "\n".join(cmds_results)
    return (f"""\n### {title}\n{results}\n""")

# if __name__ == "__main__":
#     begin = test.index("```json") + len("```json")
#     print(begin)
#     end = test.index("```", begin + len("```json"))
#     print(end)
#     print(test[begin:end])