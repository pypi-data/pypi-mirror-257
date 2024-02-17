from copy import deepcopy
from enum import Enum

import instructor
import litellm
import tiktoken
from litellm import completion
from openai import OpenAI
from termcolor import colored

from .message import MESSAGES_TYPE, assistant_message
from .utils import retry_attempts

litellm.drop_params = True


class ModelName(str, Enum):
    GPT_3 = "gpt-3.5-turbo-0125"
    GPT_4 = "gpt-4-turbo-preview"
    GEMINI = "gemini/gemini-pro"
    CLAUDE = "claude-2.1"
    MISTRAL = "anyscale/mistralai/Mistral-7B-Instruct-v0.1"
    MIXTRAL = "anyscale/mistralai/Mixtral-8x7B-Instruct-v0.1"


GPT_MODEL = ModelName.GPT_3
GEMINI_MODEL = ModelName.GEMINI


def oai_response(response) -> str:
    try:
        return response.choices[0].message.content
    except Exception:
        return response


def ask_litellm(
    messages: MESSAGES_TYPE,
    model: str = GEMINI_MODEL,
    json_mode: bool | None = None,
) -> MESSAGES_TYPE:
    try:
        if json_mode is None and "json" in messages[-1]["content"].lower():
            response_format = {"type": "json_object"}
        else:
            response_format = None
        # response_format = {
        #     "type": (
        #         "json_object"
        #         if json_mode is None and "json" in messages[-1]["content"].lower()
        #         else "text"
        #     )
        # }
        answer = oai_response(
            completion(
                messages=deepcopy(messages),
                model=model,
                response_format=response_format,
            )
        )
        messages.append(assistant_message(content=answer))
        return messages
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return messages


def count_gpt_tokens(text: str, model: str = GPT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


# @process_messages
def ask_oai(
    messages: MESSAGES_TYPE,
    model: str = GPT_MODEL,
    response_model=None,
    temperature: float = 0.3,
    patch_mode=instructor.Mode.TOOLS,
    attempts: int = 1,
    api_key: str | None = None,
    base_url: str | None = None,
) -> str:
    """Ask OpenAI to generate a response to the given messages."""
    # print(f"\n\nMESSAGES: {messages}\n\n")
    gpt = instructor.patch(OpenAI(api_key=api_key, base_url=base_url), mode=patch_mode)
    try:
        answer = gpt.chat.completions.create(
            messages=deepcopy(messages),
            model=model,
            response_model=response_model,
            temperature=temperature,
            max_retries=retry_attempts(attempts=attempts),
        )
    except Exception as e:
        print(colored(f"\n\n{model} ERROR: {e}\n\n", "red"))
        return messages
    if not response_model:
        answer = oai_response(answer)
        messages.append(assistant_message(content=answer))
        return messages
    messages.append(assistant_message(content=answer.model_dump_json()))
    return answer
