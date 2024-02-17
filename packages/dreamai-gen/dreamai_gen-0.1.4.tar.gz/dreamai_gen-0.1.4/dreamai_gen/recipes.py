from functools import partial
from typing import Any, Callable

from .llms import ModelName, ask_litellm
from .message import del_messages, set_user_role
from .prompting.edu_prompt_strs import (
    mcq_prompt,
    quiz_format_prompt,
    slides_format_prompt,
    slides_prompt,
)
from .prompting.prompt_strs import gen_rag_query_prompt, improve_prompt
from .tools import upload_quiz, upload_slides

ASKER = partial(ask_litellm, model=ModelName.GEMINI)


def re_prompt_recipe(prompt=improve_prompt, asker: Callable = ASKER):
    return [prompt, asker, partial(del_messages, idx=[-2, -3]), set_user_role]


improve_prompt_recipe = partial(re_prompt_recipe, prompt=improve_prompt)


def gen_rag_query_then_retrieve_recipe(retriever: Callable, asker: Callable = ASKER):
    return [gen_rag_query_prompt, asker, retriever, partial(del_messages, idx=[-2, -3])]


def slides_recipe(
    course_name: str,
    lesson_name: str,
    lesson_prompt: str,
    slides_service: Any,
    asker: Callable = ASKER,
    retriever: Callable | None = None,
):
    lesson_slides_creator = partial(
        upload_slides,
        name=f"{course_name}-{lesson_name}",
        title=lesson_name,
        subtitle="",
        service=slides_service,
    )
    recipe = [
        lesson_prompt,
        slides_prompt,
        "You MUST give me at least 4 bullet points for per slide.",
        asker,
        slides_format_prompt,
        {f"{'_'.join(lesson_name.split())}_slides": asker},
        {"slides_id": lesson_slides_creator},
    ]
    if retriever:
        recipe.insert(
            2, gen_rag_query_then_retrieve_recipe(retriever=retriever, asker=asker)
        )
    return recipe


def quiz_recipe(
    course_name: str, lesson_name: str, forms_service: Any, asker: Callable = ASKER
):
    lesson_quiz_creator = partial(
        upload_quiz,
        name=f"{course_name}-{lesson_name}",
        title=lesson_name,
        service=forms_service,
    )

    return [
        # partial(print, "Creating a quiz...⏳"),
        mcq_prompt,
        "You MUST give me at least 10 MCQs based on the lesson above.",
        # asker,
        quiz_format_prompt,
        {f"{'_'.join(lesson_name.split())}_quiz": asker},
        {"quiz_id": lesson_quiz_creator},
    ]


# rephrase_rag_query_tasks = partial(
# re_prompt_tasks,
# prompt=rephrase_rag_query_prompt,
# )
