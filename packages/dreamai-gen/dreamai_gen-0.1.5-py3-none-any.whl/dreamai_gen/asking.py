import copy
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, Callable

from tenacity import RetryError, Retrying, stop_after_attempt
from termcolor import colored

from . import prompting
from .llms import ask_oai
from .message import MESSAGES_TYPE, last_user_message, user_message
from .prompting.prompt_fns import (
    chat_template,
    create_template_functions,
    path_selection_template,
    process_prompt,
)
from .tools import use_tool
from .utils import flatten_list

TEMPLATE_FUNCTIONS = create_template_functions([prompting])
ASKER = ask_oai


def noop(x=None, **kwargs):
    return x


# @process_messages
def check_exit(messages: MESSAGES_TYPE = None) -> bool:
    if not messages:
        return False
    last_content = messages[-1]["content"]
    if isinstance(last_content, str) and last_content.lower() == "exit":
        messages.pop(-1)
        return True
    last_user_msg = last_user_message(messages)
    if last_user_msg:
        last_user_content = last_user_msg["message"]["content"]
        if isinstance(last_user_content, str) and last_user_content.lower() == "exit":
            messages.pop(last_user_msg["index"])
            return True
    return False


def run_task(task, assets: dict | None = None, asset_key: str | None = None) -> dict:
    if asset_key and asset_key == "skip":
        return assets
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    if isinstance(task, dict):
        return run_dict_task(task, assets)
    return run_list_task(task, assets, asset_key)


def run_dict_task(task: dict, assets: dict) -> dict:
    for asset_key, subtask in task.items():
        assets = run_task(
            task=subtask,
            assets=assets,
            asset_key=asset_key,
        )
    return assets


def run_list_task(task, assets: dict, asset_key: str | None = None) -> dict:
    task = [task] if not isinstance(task, list) else task
    task = flatten_list(task)
    for subtask in task:
        if check_exit(assets["messages"]):
            break
        if isinstance(subtask, dict):
            current_asset_key, subtask = list(subtask.items())[0]
        else:
            current_asset_key = asset_key
        assets = process_subtask(subtask, assets, current_asset_key)
    return assets


def process_subtask(subtask, assets: dict, asset_key: str | None = None) -> dict:
    if callable(subtask):
        assets = use_tool(
            tool=subtask,
            assets=assets,
            asset_key=asset_key,
        )
    elif isinstance(subtask, (str, Path)):
        task_content = process_prompt(subtask, template_functions=TEMPLATE_FUNCTIONS)
        assets["messages"].append(user_message(content=task_content))
        if asset_key:
            assets[asset_key] = task_content
    else:
        raise TypeError(f"Invalid task type: {type(subtask)}")
    return assets


# def run_task(task, assets: dict | None = None, asset_key: str | None = None) -> dict:
#     if asset_key and asset_key == "skip":
#         return assets
#     assets = assets or OrderedDict()
#     assets.setdefault("messages", [])
#     if isinstance(task, dict):
#         for asset_key, subtask in task.items():
#             assets = run_task(
#                 task=subtask,
#                 assets=assets,
#                 asset_key=asset_key,
#             )
#         return assets
#     if not isinstance(task, list):
#         task = [task]
#     task = flatten_list(task)
#     for subtask in task:
#         if check_exit(assets["messages"]):
#             break
#         if isinstance(subtask, dict):
#             asset_key, subtask = list(subtask.items())[0]
#         if callable(subtask):
#             assets = use_tool(
#                 tool=subtask,
#                 assets=assets,
#                 asset_key=asset_key,
#             )
#         elif isinstance(subtask, (str, Path)):
#             task_content = process_prompt(
#                 subtask, template_functions=TEMPLATE_FUNCTIONS
#             )
#             assets["messages"].append(user_message(content=task_content))
#             if asset_key:
#                 assets[asset_key] = task_content
#         else:
#             raise TypeError(f"Invalid task type: {type(subtask)}")
#     return assets


def _decide(messages: MESSAGES_TYPE, asker: Callable = ASKER):
    res = (
        asker(messages=messages)[-1]["content"]
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    print(f"\n\nDECIDE RES: {res}\n\n")
    return json.loads(res)["path_index"]


def decide(
    paths_dict: dict[str, Any],
    assets: dict | None = None,
    asker: Callable = ASKER,
    history_len: int = 3,
    optional: bool = False,
    attempts: int = 2,
) -> dict:
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    decide_messages = copy.deepcopy(assets["messages"])
    path_descs = []
    paths = []
    for path_desc, path in paths_dict.items():
        path_descs.append(path_desc)
        paths.append(path)
    if optional:
        path_descs.append("No Tasks")
        paths.append([noop])
    if history_len == 0:
        chat_history = ""
    elif history_len == -1:
        chat_history = chat_template(decide_messages)
    else:
        chat_history = chat_template(decide_messages[-history_len:])
    # print(f"\n\nCHAT HISTORY: {chat_history}\n\n")
    # print(f"\n\nLAST MESSAGE: {decide_messages[-1]['content']}\n\n")
    # print(f"\n\nPATH DESCRIPTIONS: {path_descs}\n\n")
    path_selection_message = user_message(
        content=path_selection_template(
            path_descs=path_descs, chat_history=chat_history
        )
    )
    print(f"\n\nPATH SELECTION MESSAGE: {path_selection_message['content']}\n\n")
    decide_messages.append(path_selection_message)
    try:
        for attempt in Retrying(stop=stop_after_attempt(attempts)):
            with attempt:
                path_index = _decide(messages=decide_messages, asker=asker)
                path = paths[path_index]
    except RetryError:
        path = [noop]
    return run_task(task=path, assets=assets)


def ask(*tasks, assets: dict | None = None) -> dict:
    assets = assets or OrderedDict()
    assets.setdefault("messages", [])
    messages = assets["messages"]
    tasks = list(tasks)
    # print(f"\n\nASK TASKS: {tasks}\n\n")
    # print(f"\n\nASK MESSAGES: {messages}\n\n")
    if len(messages) > 0 and messages[-1]["role"] == "user":
        if tasks[0] != messages[-1]["content"]:
            tasks.insert(0, messages.pop(-1)["content"])
    for task in tasks:
        try:
            assets = run_task(task=task, assets=assets)
        except Exception as e:
            print(colored(f"\n\nASK ERROR: {e}\n\n", "red"))
        if check_exit(assets["messages"]):
            break
    return assets
