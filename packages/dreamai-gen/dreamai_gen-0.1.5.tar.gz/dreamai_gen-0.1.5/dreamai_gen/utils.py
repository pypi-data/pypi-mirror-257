import inspect
import re
import textwrap
import typing
from datetime import datetime
from functools import partial
from inspect import cleandoc
from itertools import chain
from pathlib import Path
from typing import Callable

import demoji
from fastcore.basics import flatten
from IPython.display import Markdown
from tenacity import Retrying, stop_after_attempt, wait_random
from unstructured.cleaners.core import (
    bytes_string_to_string,
    clean_non_ascii_chars,
    group_broken_paragraphs,
    group_bullet_paragraph,
    replace_mime_encodings,
    replace_unicode_quotes,
)


def resolve_data_path(data_path: list | str | Path) -> chain:
    if not isinstance(data_path, list):
        data_path = [data_path]
    data_path = flatten(data_path)
    paths = []
    for dp in data_path:
        if isinstance(dp, (str, Path)):
            dp = Path(dp)
            if not dp.exists():
                raise Exception(f"Path {dp} does not exist.")
            if dp.is_dir():
                paths.append(dp.iterdir())
            else:
                paths.append([dp])
    return chain(*paths)


def flatten_list(my_list: list) -> list:
    """Flatten a list of lists."""
    new_list = []
    for x in my_list:
        if isinstance(x, list):
            new_list += flatten_list(x)
        else:
            new_list.append(x)
    return new_list


def retry_attempts(attempts: int = 3):
    return (
        Retrying(wait=wait_random(min=1, max=40), stop=stop_after_attempt(attempts))
        if attempts > 1
        else 1
    )


def deindent(text: str) -> str:
    return textwrap.dedent(cleandoc(text))


def clean_text(text: str, include_emojis: bool = True, group: bool = False) -> str:
    text = re.sub(r"[\n+]", "\n", text)
    text = re.sub(r"[\t+]", " ", text)
    text = re.sub(r"[. .]", " ", text)
    text = re.sub(r"([ ]{2,})", " ", text)
    # print(text)
    try:
        text = bytes_string_to_string(text)
        # print(text)
    except Exception:
        pass
    try:
        text = clean_non_ascii_chars(text)
        # print(text)
    except Exception:
        pass
    try:
        text = replace_unicode_quotes(text)
        # print(text)
    except Exception:
        pass
    try:
        text = replace_mime_encodings(text)
        # print(text)
    except Exception:
        pass
    if group:
        try:
            text = "\n".join(group_bullet_paragraph(text))
            # print(text)
        except Exception:
            pass
        try:
            text = group_broken_paragraphs(text)
            # print(text)
        except Exception:
            pass
    if not include_emojis:
        text = demoji.replace(text, "")
    return text


def get_param_names(func: Callable):
    func = func.func if type(func) == partial else func
    return inspect.signature(func).parameters.keys()


def get_required_param_names(func: Callable) -> list[str]:
    if type(func) == partial:
        params = inspect.signature(func.func).parameters
        return [
            name
            for name, param in params.items()
            if param.default == inspect.Parameter.empty
            and name not in func.keywords.keys()
        ]
    params = inspect.signature(func).parameters
    return [
        name
        for name, param in params.items()
        if param.default == inspect.Parameter.empty
    ]


def get_function_return_type(func: Callable) -> type:
    func = func.func if type(func) == partial else func
    sig = typing.get_type_hints(func)
    return sig.get("return", None)


def get_function_name(func: Callable) -> str:
    func = func.func if type(func) == partial else func
    return func.__name__


def get_function_source(func: Callable) -> str:
    if type(func) == partial:
        func = func.func
    return inspect.getsource(func)


def get_function_info(func: Callable) -> str:
    """Get a string with the name, signature, and docstring of a function."""

    func = func.func if type(func) == partial else func
    name = func.__name__
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func)
    desc = f"\n---\nA function:\nName: {name}\n"
    if signature:
        desc += f"Signature: {signature}\n"
    if docstring:
        desc += f"Docstring: {docstring}\n"
    return cleandoc(desc + "---\n\n")


def to_markdown(text: str) -> Markdown:
    return Markdown(
        textwrap.indent(text.replace("•", "  *"), "> ", predicate=lambda _: True)
    )


def current_time(format: str = "%m-%d-%Y_%H:%M:%S") -> str:
    # print(f"\n\nCURRENT TIME: {datetime.now().strftime(format)}\n\n")
    return datetime.now().strftime(format)


def sort_times(times, format="%m-%d-%Y_%H:%M:%S"):
    return sorted(times, key=lambda time: datetime.strptime(time, format))


def count_words(text: str) -> int:
    return len(text.split())


def count_lines(text: str) -> int:
    return len(text.split("\n"))


def token_count_to_word_count(token_count) -> int:
    return max(int(token_count * 0.75), 1)


def token_count_to_line_count(token_count) -> int:
    return max(int(token_count * 0.066), 1)


def word_count_to_token_count(word_count) -> int:
    return max(int(word_count / 0.75), 1)


def count_tokens(text: str) -> int:
    return word_count_to_token_count(len(text.split()))
