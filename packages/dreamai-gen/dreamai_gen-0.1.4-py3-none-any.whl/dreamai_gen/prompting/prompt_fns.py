import inspect
import json
import os
from pathlib import Path
from typing import Callable

from termcolor import colored

from ..utils import deindent
from .prompt_strs import path_selection_prompt


def create_template_functions(modules: list) -> dict[str, Callable]:
    template_functions = {}
    for module in modules:
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            if name.endswith("_template"):
                template_functions[name] = fn
    return template_functions


def json_to_prompt(
    prompt_file: str | Path, template_functions: dict[str, Callable] | None = None
) -> str:
    if not os.path.exists(prompt_file := str(prompt_file)):
        return ""
    with open(prompt_file, "r") as f:
        prompt_data = json.load(f)
    # print(f"\n\nPROMPT DATA: {prompt_data}\n\n")
    if template_functions is None or "template_function" not in prompt_data:
        if "template_args" in prompt_data:
            template_args = prompt_data["template_args"]
        else:
            template_args = prompt_data
        if isinstance(template_args, dict) and "titles_dict" not in template_args:
            template_args = {"titles_dict": template_args}
        return titles_w_content_template(**template_args)
    template_function = template_functions[prompt_data["template_function"]]
    # print(f"\n\nTEMPLATE ARGS: {prompt_data['template_args']}\n\n")
    return template_function(**prompt_data["template_args"])


def txt_to_prompt(prompt_file: str | Path) -> str:
    if not os.path.exists(prompt_file := str(prompt_file)):
        return ""
    with open(prompt_file, "r") as f:
        prompt = f.read()
    return deindent(prompt)


def process_prompt(
    prompt: str | Path | list[str],
    template_functions: dict[str, Callable] | None = None,
) -> str:
    if not prompt:
        return ""
    if isinstance(prompt, list):
        prompt = "\n\n---\n\n".join(list(prompt))
    elif isinstance(prompt, (Path, str)):
        prompt = str(prompt)
        if prompt.endswith(".txt"):
            prompt = txt_to_prompt(prompt)
        elif prompt.endswith(".json"):
            prompt = json_to_prompt(prompt, template_functions=template_functions)
    return deindent(str(prompt))


def titles_w_content_template(
    titles_dict: dict[str, str | Path | list[str]] = {},
    prefix: str = "",
    suffix: str = "",
) -> str:
    prompt = deindent(prefix)
    for title, content in titles_dict.items():
        if content:
            title = " ".join(title.split("_")).strip().title()
            content = process_prompt(content)
            if content:
                if len(prompt) > 0:
                    prompt += "\n\n"
                prompt += deindent(f"## {title} ##\n\n{deindent(content)}")
    prompt += "\n\n" + deindent(suffix)
    return deindent(prompt)


def rag_template(info: str | list[str], prefix: str = "") -> str:
    return titles_w_content_template(
        titles_dict={"retrieved information": info},
        prefix=prefix or "Get help from this retrieved information for your response.",
    )


def message_template(message: dict[str, str]) -> str:
    assert "role" in message and ("content" in message or "parts" in message)
    role = message["role"]
    content = message["content"] if "content" in message else message["parts"]
    return deindent(f"## {role.upper()} ##\n\n{content}")


def chat_template(messages: list[dict[str, str]], with_colors=False) -> str:
    role_to_color = {
        "system": "cyan",
        "user": "cyan",
        "assistant": "green",
    }
    chat = []
    for message in messages:
        message_str = message_template(message)
        if with_colors:
            message_str = colored(message_str, role_to_color[message["role"]])
        chat.append(message_str)
    return deindent("\n\n".join(chat))


def path_selection_template(
    path_descs: list[str], paths_prompt: str = "", chat_history: str = ""
) -> str:
    return titles_w_content_template(
        {
            "Conversation History": deindent(chat_history),
            "Path Descriptions": titles_w_content_template(
                {f"Path {i}": path_desc for i, path_desc in enumerate(path_descs)}
            ),
        },
        prefix=deindent(paths_prompt or path_selection_prompt) + "\n\n",
    )


def gen_web_search_query_template(n_queries: int = 3):
    return deindent(
        f"""
        You are an expert at web search.
        I need {n_queries} web search queries based on the messages above. The messages are part of an ongoing conversation so they may have some unnecessary text like "Okay so tell me about...", "I want to know about...", "I'm curious about...", etc.
        Give me effective queries for a web search engine like Google, Bing, DuckDuckGo, etc.
        I will use your queries as they are, so please don't add any comments or notes or prefacing or ending statements.
        Thank you!
        """
    )


def generic_summary_template(line_count: int = 10) -> str:
    return deindent(
        f"""
    As a professional summarizer, create a concise and comprehensive summary of the provided text, be it an article, post, conversation, or passage, while adhering to these guidelines:
    1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
    2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
    3. Keep all the important information in the summary.
    4. Rely strictly on the provided text, without including external information.
    5. Format the summary in paragraph form for easy understanding.
    6. It should be no more than {line_count} lines long.
    """
    )


def repeat_template(num_steps: int = 1) -> str:
    if num_steps == 1:
        return "Repeat the previous step that you did for this new prompt."
    else:
        return (
            f"Repeat the previous {num_steps} steps that you did for this new prompt."
        )
