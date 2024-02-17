import json
import re
from collections import Counter, OrderedDict
from copy import deepcopy
from typing import Any, Callable

import pandas as pd
import torch
from langchain.tools.brave_search.tool import BraveSearch
from langchain.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain.utilities.python import PythonREPL
from sentence_transformers import CrossEncoder
from termcolor import colored

from .chroma import ChromaCollection
from .g_apis.quiz import add_question, create_quiz
from .g_apis.slides import add_slide, create_presentation
from .message import MESSAGES_TYPE, assistant_message, user_message
from .prompting.prompt_fns import (
    chat_template,
    generic_summary_template,
    rag_template,
    titles_w_content_template,
)
from .utils import (
    count_tokens,
    get_function_name,
    get_param_names,
    get_required_param_names,
    token_count_to_line_count,
)

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
MAX_TOKENS = 25_000


# @retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def use_tool(
    tool: Callable,
    assets: dict | None = None,
    asset_key: str | None = None,
    **kwargs,
) -> dict:
    assets = OrderedDict(assets) or OrderedDict()
    assets.setdefault("messages", [])
    params = {**assets, **kwargs}
    tool_name = get_function_name(tool)
    tool_params = get_param_names(tool)
    tool_required_params = get_required_param_names(tool)
    # print(f"\n\nTOOL: {tool_name}\n\n")
    if "kwargs" in tool_params:
        call_params = params
    else:
        call_params = {k: v for k, v in params.items() if k in tool_params}
    if "assets" in tool_params:
        call_params["assets"] = assets
    if call_params or not tool_required_params:
        curr_messages = deepcopy(assets["messages"])
        try:
            ret = tool(**call_params)
        except Exception as e:
            error_msg = f"ERROR WITH TOOL: {tool_name}\nERROR: {e}"
            print(colored(f"\n\n{error_msg}\n\n", "red"))
            # assets["messages"].append(
            #     user_message(
            #         content=f"ERROR WITH TOOL: {get_function_source(tool)}\nERROR: {e}"
            #     )
            # )
            ret = None
        try:
            if ret is not None:
                asset_key = asset_key or f"{tool_name}_result"
                ret_dict = {asset_key: ret}
                # print(f"\n\nRET: {ret}\n\n")
                # print(f"\n\nASSETS: {assets}\n\n")
                # print(f"\n\nCURR MESSAGES: {curr_messages}\n\n")
                if (
                    assets["messages"] != curr_messages
                ):  # the tool modified the messages
                    if (
                        ret == assets["messages"]
                    ):  # the tool returned the modified messages
                        ret_dict = {asset_key: ret[-1]["content"]}
                    elif (
                        ret != assets["messages"][-1]["content"]
                    ):  # the tool modified the messages and also returned something else
                        ret_dict = {
                            asset_key: ret,
                            f"{asset_key}_message": assets["messages"][-1]["content"],
                        }
                elif ret == assets["messages"]:  # nothing was modified
                    ret_dict = {}
                assets.update(ret_dict)
        except Exception as e:
            error_msg = f"ERROR WITH TOOL RESULT: {tool_name}\nERROR: {e}"
            print(colored(f"\n\n{error_msg}\n\n", "red"))
            # assets["messages"].append(
            #     user_message(
            #         content=f"ERROR WITH TOOL RESULT: {get_function_source(tool)}\nERROR: {e}"
            #     )
            # )
    return assets


def format_brave_snippets(snippets, start=1):
    ret = ""
    for i, s in enumerate(snippets, start=start):
        title = s["title"]
        snippet = s["snippet"]
        snippet = re.sub(
            r"<strong>(.*?)</strong>", lambda x: x.group(1).upper(), snippet
        )
        ret += f"[{i}] {title}\n"
        ret += f"{snippet}\n\n"
    return ret


# @process_messages
def brave_search(
    messages: MESSAGES_TYPE = None, query: str = "", count: int = 5
) -> MESSAGES_TYPE:
    """Query the Brave web search API and add the results to the messages list."""
    if not messages:
        return []
    if not query:
        return messages
    search = BraveSearch.from_api_key(
        api_key="BSAYt3qZcqqKxxuFTEZeA7BL0EiRmqs", search_kwargs={"count": count}
    )
    query = query or messages[-1]["content"]
    # print(f"\n\nQUERY: {query}\n\n")
    res = json.loads(search.run(query))
    # print(f"\n\nBRAVE SEARCH RESULTS: {res}\n\n")
    messages.append(
        user_message(
            content=titles_w_content_template(
                {"Up to date Web Search Results For You": format_brave_snippets(res)}
            )
        )
    )
    return messages


# @process_messages
def ddg_search(messages: MESSAGES_TYPE = None, query: str = "") -> MESSAGES_TYPE:
    """
    Query the DuckDuckGo web search API and add the results to the messages list.
    If there are no good results, try Brave Search.
    """

    if not messages:
        return []
    if not query:
        return messages
    search = DuckDuckGoSearchRun()
    query = query or messages[-1]["content"]
    print(f"\n\nQUERY: {query}\n\n")
    res = search.run(query)
    if "No good DuckDuckGo Search Result was found" in res:
        return brave_search(messages=messages, query=query)
    messages.append(
        user_message(
            content=titles_w_content_template(
                {"Up to date Web Search Results For Your Task": res}
            )
        )
    )
    return messages


# @process_messages
def upload_slides(
    messages: MESSAGES_TYPE,
    service: Any,
    name: str = "DREAMAI SLIDES",
    title: str = "DREAMAI",
    subtitle: str = "",
) -> str | None:
    if not messages:
        return None
    course = json.loads(messages[-1]["content"])
    presentation_id = create_presentation(
        service=service,
        name=name,
        title=title,
        subtitle=subtitle,
    )
    [
        add_slide(
            service=service,
            presentation_id=presentation_id,
            title_text=title,
            body_text=bullets,
        )
        for title, bullets in zip(course["titles"], course["bullets"])
    ]
    return presentation_id


# @process_messages
def upload_quiz(
    messages: MESSAGES_TYPE,
    service: Any,
    name: str = "DREAMAI QUIZ",
    title: str = "DREAMAI",
) -> str | None:
    if not messages:
        return None
    quiz = json.loads(messages[-1]["content"])
    quiz_id = create_quiz(
        service=service,
        name=name,
        title=title,
    )
    [
        add_question(
            question=question,
            answers=answers,
            correct_index=correct_index,
            service=service,
            quiz_id=quiz_id,
        )
        for question, answers, correct_index in zip(
            quiz["questions"], quiz["answers"], quiz["correct_indices"]
        )
    ]
    return quiz_id


# @process_messages
def user_feedback(
    messages: MESSAGES_TYPE = None,
    asssistant_query: str = "",
    history_len: int = 2,
) -> MESSAGES_TYPE:
    """Get user feedback on a list of messages."""
    if not messages:
        return []
    if history_len > 0:
        print(chat_template(messages[-history_len:], with_colors=True))
    if asssistant_query:
        messages.append(assistant_message(content=asssistant_query))
    user_response = input(f"{asssistant_query}\n")
    messages.append(user_message(content=user_response))
    return messages


# @process_messages
def run_code(
    messages: MESSAGES_TYPE = None,
    code: str = "",
    _globals: dict | None = None,
    _locals: dict | None = None,
) -> MESSAGES_TYPE:
    """Run code in a Python REPL and add the result to the messages list."""
    if not messages:
        return []
    python_repl = PythonREPL(_globals=_globals, _locals=_locals)
    if not code:
        code = next(
            (
                message["content"]
                for message in reversed(messages)
                if "```python" in message["content"]
            ),
            None,
        )
        if not code:
            return messages
    try:
        code = code.split("```python")[1].split("```")[0].strip()
        code_result = python_repl.run(code)
    except Exception as e:
        code_result = str(e)
    if code_result:
        messages.append(assistant_message(content=code_result))
    return messages


# @process_messages
def chroma_retriever(
    messages: MESSAGES_TYPE,
    collection: ChromaCollection,
    n_results: int = 10,
    **kwargs,
) -> MESSAGES_TYPE:
    """Query the Chroma collection with the last message as the query text."""
    if not messages:
        return []
    query_text = messages[-1]["content"]
    query_res = collection.query(query_texts=query_text, n_results=n_results)
    messages.append(user_message(content=rag_template(info=query_res["documents"][0])))
    return messages


def rerank_chroma_results(
    query_text: str,
    results: dict,
    n_rerank: int = 40,
    cross_encoder_model: str = CROSS_ENCODER_MODEL,
) -> dict:
    """Rerank the results with a cross-encoder model."""
    if n_rerank:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        cross_encoder = CrossEncoder(cross_encoder_model, device=device)
        pairs = [[query_text, doc] for doc in results["documents"][0]]
        scores = cross_encoder.predict(pairs)
        scores_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        results = {k: [[v[0][i] for i in scores_idx]] for k, v in results.items()}
    return results


def chroma_family_retreiver_2(
    query_text: str,
    children_collection: ChromaCollection,
    parents_df: pd.DataFrame | None = None,
    n_children: int = 100,
    n_rerank: int = 50,
    children_per_parent: int = 2,
    metadata_filter: dict | None = None,
    only_get: bool = False,
) -> str:
    if only_get and metadata_filter is not None:
        children = children_collection.get(where=metadata_filter)
        children_ids = children["ids"]
        children_docs = children["documents"]
        children_metadatas = children["metadatas"]
        print(f"\n\nQUERIED CHILDREN: {children['ids']}\n\n")
    elif not query_text:
        return ""
    else:
        print(f"\n\nQUERY TEXT: {query_text}\n\n")
        children = children_collection.query(
            query_texts=query_text, n_results=n_children, where=metadata_filter
        )
        print(f"\n\nQUERIED CHILDREN: {children['ids'][0]}\n\n")
        children = rerank_chroma_results(
            results=children, query_text=query_text, n_rerank=n_rerank
        )
        children_ids = children["ids"][0]
        children_docs = children["documents"][0]
        children_metadatas = children["metadatas"][0]
    print(f"\n\nCHILDREN: {children_ids}\n\n")
    if len(parents_df) == 0:
        parents = children_docs
    else:
        children_file_pages = [
            (metadata["filename"], metadata["page_number"])
            for metadata in children_metadatas
        ]
        children_file_page_counts = Counter(children_file_pages)
        parents_file_pages = sorted(
            [
                file_page
                for file_page, count in children_file_page_counts.items()
                if count >= children_per_parent
            ],
            key=lambda x: x[1],
        )
        print(f"\n\nPARENTS FILE PAGES: {parents_file_pages}\n\n")
        parents_file_pages = parents_file_pages or children_file_pages
        parents = parents_df[
            parents_df.apply(
                lambda row: (row["filename"], row["page_number"]) in parents_file_pages,
                axis=1,
            )
        ]["page_content"].tolist()
    return "\n\n".join(parents) if parents else ""


# @process_messages
def chroma_family_retreiver(
    messages: MESSAGES_TYPE,
    children_collection: ChromaCollection,
    parents_df: pd.DataFrame | None = None,
    n_children: int = 100,
    n_rerank: int = 50,
    children_per_parent: int = 2,
    metadata_filter: dict | None = None,
    only_get: bool = False,
) -> MESSAGES_TYPE:
    """Query the children collection with the last message as the query text and then retrieve the parents."""
    if only_get and metadata_filter is not None:
        children = children_collection.get(where=metadata_filter)
        children_ids = children["ids"]
        children_docs = children["documents"]
        children_metadatas = children["metadatas"]
        print(f"\n\nQUERIED CHILDREN: {children['ids']}\n\n")
        messages = messages or []
    elif not messages:
        return []
    else:
        query_text = messages[-1]["content"]
        print(f"\n\nQUERY TEXT: {query_text}\n\n")
        children = children_collection.query(
            query_texts=query_text, n_results=n_children, where=metadata_filter
        )
        print(f"\n\nQUERIED CHILDREN: {children['ids'][0]}\n\n")
        children = rerank_chroma_results(
            results=children, query_text=query_text, n_rerank=n_rerank
        )
        children_ids = children["ids"][0]
        children_docs = children["documents"][0]
        children_metadatas = children["metadatas"][0]
    print(f"\n\nCHILDREN: {children_ids}\n\n")
    if len(parents_df) == 0:
        parents = children_docs
    else:
        children_file_pages = [
            (metadata["filename"], metadata["page_number"])
            for metadata in children_metadatas
        ]
        children_file_page_counts = Counter(children_file_pages)
        parents_file_pages = sorted(
            [
                file_page
                for file_page, count in children_file_page_counts.items()
                if count >= children_per_parent
            ],
            key=lambda x: x[1],
        )
        print(f"\n\nPARENTS FILE PAGES: {parents_file_pages}\n\n")
        parents_file_pages = parents_file_pages or children_file_pages
        parents = parents_df[
            parents_df.apply(
                lambda row: (row["filename"], row["page_number"]) in parents_file_pages,
                axis=1,
            )
        ]["page_content"].tolist()
    if parents:
        messages.append(user_message(content=rag_template(info=parents)))
    return messages


# @process_messages
def summarize_messages(
    messages: MESSAGES_TYPE,
    asker: Callable,
    max_tokens: int = MAX_TOKENS,
    **kwargs,
) -> MESSAGES_TYPE:
    """Summarize the chat if it is longer than max_tokens."""
    if not messages:
        return []
    if count_tokens(chat_template(messages)) <= max_tokens:
        return messages
    line_count = token_count_to_line_count(max_tokens)
    system_msg = None
    user_msg = None
    if messages[0]["role"] == "system":
        system_msg = messages.pop(0)
    if len(messages) > 1 and messages[-1]["role"] == "user":
        other_messages = messages[:-1]
        user_msg = messages[-1]
        other_messages_token_count = count_tokens(chat_template(other_messages))
        user_msg_token_count = count_tokens(user_msg["content"])
        if user_msg_token_count < other_messages_token_count:
            user_msg = messages.pop(-1)
        else:
            user_msg = None

    if not messages:
        return [message for message in [system_msg, user_msg] if message]

    chat_str = chat_template(messages)
    summary_prompt = titles_w_content_template(
        titles_dict={
            "conversation": chat_str,
            "task": generic_summary_template(line_count=line_count),
        },
        # suffix=generic_summary_template(line_count=line_count),
    )
    messages = [user_message(content=summary_prompt)]
    print(f"\n\nSUMMARY PROMPT: {summary_prompt}\n\n")
    messages = asker(messages=messages)
    chat_summary = messages[-1]["content"]
    messages = [
        user_message(
            content=titles_w_content_template(
                titles_dict={"chat_summary": chat_summary}
            )
        )
    ]
    if system_msg:
        messages.insert(0, system_msg)
    if user_msg:
        messages.append(user_msg)
    return messages


# @process_messages
def summarize_then_ask(
    messages: MESSAGES_TYPE,
    asker: Callable,
    max_tokens: int = MAX_TOKENS,
    **kwargs,
) -> MESSAGES_TYPE:
    """Summarize the chat if it is longer than max_tokens and then ask a question."""
    if not messages:
        return []
    messages = summarize_messages(messages=messages, asker=asker, max_tokens=max_tokens)
    return asker(messages=messages)
