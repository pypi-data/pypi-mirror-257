import inspect
import json
import os
from collections import OrderedDict
from functools import wraps
from pathlib import Path
from typing import Callable

from .utils import current_time, sort_times

DEFAULT_ROLE = "user"
MESSAGE_TYPE = dict[str, str]
MESSAGES_TYPE = list[MESSAGE_TYPE] | None
# MESSAGES_TYPE = list[dict[str, str]]


def chat_message(role: str, content: str) -> dict[str, str]:
    return {"role": role, "content": content}


def system_message(content: str) -> dict[str, str]:
    return chat_message(role="system", content=content)


def user_message(content: str) -> dict[str, str]:
    return chat_message(role="user", content=content)


def assistant_message(content: str) -> dict[str, str]:
    return chat_message(role="assistant", content=content)


def str_to_messages(messages: MESSAGES_TYPE) -> MESSAGES_TYPE:
    messages = [messages] if not isinstance(messages, list) else messages
    for i, message in enumerate(messages):
        if isinstance(message, str):
            messages[i] = user_message(content=message)
        elif not isinstance(message, dict):
            raise TypeError(f"Invalid message type: {type(message)}")
    return messages


def process_messages(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = inspect.getcallargs(func, *args, **kwargs)
        if not (messages := kwargs.get("messages")):
            return []
        messages = str_to_messages(messages)
        kwargs["messages"] = messages
        return func(**kwargs)

    original_signature = inspect.signature(func)
    wrapper.__annotations__ = {
        k: v.annotation
        for k, v in original_signature.parameters.items()
        if v.annotation is not inspect.Parameter.empty
    }
    if original_signature.return_annotation is not inspect.Signature.empty:
        wrapper.__annotations__["return"] = original_signature.return_annotation

    return wrapper


def last_message(
    messages: MESSAGES_TYPE, role: str = ""
) -> dict[str, int | dict[str, str]]:
    """Returns the last message with the given role."""

    if role:
        messages = [
            [i, message]
            for i, message in enumerate(messages)
            if message["role"] == role
        ]
    if len(messages) == 0:
        return None
    else:
        return {"index": messages[-1][0], "message": messages[-1][1]}


def last_user_message(messages: MESSAGES_TYPE) -> dict:
    message = last_message(messages, role="user")
    # print(f"Last user message: {message}")
    return message


def last_assistant_message(messages: MESSAGES_TYPE) -> dict:
    message = last_message(messages, role="assistant")
    # print(f"Last assistant message: {message}")
    return message


# @process_messages
def merge_same_role_messages(messages: MESSAGES_TYPE) -> MESSAGES_TYPE:
    if not messages:
        return []
    new_messages = []
    last_message = None
    for message in messages:
        if last_message is None:
            last_message = message
        elif last_message["role"] == message["role"]:
            last_message["content"] += "\n\n" + message["content"]
        else:
            new_messages.append(last_message)
            last_message = message
    if last_message is not None:
        new_messages.append(last_message)
    return new_messages


# @process_messages
def del_messages(messages: MESSAGES_TYPE, idx: int | list[int] = -1) -> MESSAGES_TYPE:
    """Delete the messages at the given indices."""
    if not messages:
        return []
    if not isinstance(idx, list):
        idx = [idx]
    idx = [i % len(messages) for i in idx if i < len(messages)]
    return [message for i, message in enumerate(messages) if i not in idx]


# @process_messages
def merge_n_messages(
    messages: MESSAGES_TYPE = None,
    merged_role: str = DEFAULT_ROLE,
    n_messages: int = 2,
) -> MESSAGES_TYPE:
    """Merge the last n_messages into a single message with the given role."""

    if len(messages) < n_messages:
        return messages
    last_n_messages = messages[-n_messages:]
    merged_content = "\n\n".join([m["content"] for m in last_n_messages])
    messages[-n_messages:] = [{"role": merged_role, "content": merged_content}]
    return messages


# @process_messages
def edit_messages(
    messages: MESSAGES_TYPE,
    idx: int | list[int] = -1,
    content: str | list[str] | None = None,
    role: str | list[str] | None = None,
) -> MESSAGES_TYPE:
    """Edit the messages at the given indices."""
    if not messages:
        return []
    if not isinstance(idx, list):
        idx = [idx]
    idx = [i % len(messages) for i in idx if i < len(messages)]
    for i, id in enumerate(idx):
        if content:
            if isinstance(content, list):
                messages[id]["content"] = content[i]
            else:
                messages[id]["content"] = content
        if role:
            if isinstance(role, list):
                messages[id]["role"] = role[i]
            else:
                messages[id]["role"] = role
    return messages


# @process_messages
def set_role(messages: MESSAGES_TYPE, role: str = DEFAULT_ROLE) -> MESSAGES_TYPE:
    """Set the role of the last message."""
    if not messages:
        return []
    messages[-1]["role"] = role
    return messages


def set_user_role(messages: MESSAGES_TYPE) -> MESSAGES_TYPE:
    return set_role(messages=messages, role="user")


def set_assistant_role(messages: MESSAGES_TYPE) -> MESSAGES_TYPE:
    return set_role(messages=messages, role="assistant")


def messages_to_chat(
    messages: MESSAGES_TYPE, chat_name: str = ""
) -> dict[str, list[dict[str, str]]]:
    chat_name = chat_name or current_time()
    return {chat_name: messages}


def save_chats(chats: dict[str, list[dict[str, str]]], chats_dir: str | Path = "chats"):
    os.makedirs(chats_dir, exist_ok=True)
    for chat_name, messages in chats.items():
        with open(f"{chats_dir}/{chat_name}.json", "w") as f:
            json.dump(messages, f, indent=4)


def load_chats(chats_dir: str | Path = "chats") -> dict[str, list[dict[str, str]]]:
    os.makedirs(chats_dir, exist_ok=True)
    chats = {}
    for file in Path(chats_dir).glob("*.json"):
        chat_name = Path(file).stem
        messages = json.load(file)
        chats[chat_name] = messages
    try:
        chats = OrderedDict(
            {chat_name: chats[chat_name] for chat_name in sort_times(chats.keys())}
        )
    except Exception:
        pass
    return chats
