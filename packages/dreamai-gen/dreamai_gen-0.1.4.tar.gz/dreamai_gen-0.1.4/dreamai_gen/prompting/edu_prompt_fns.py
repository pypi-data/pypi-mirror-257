from ..utils import deindent
from .edu_prompt_strs import mcq_prompt, slides_prompt
from .prompt_fns import titles_w_content_template


def course_template(course_name: str, prefix: str = "", **extra) -> str:
    prefix = (
        deindent(prefix)
        or "You are a friendly and helpful instructional coach helping teachers create engaging and effective lessons for their students."
    )
    if course_name:
        prefix += f"\nThe course you are currently coaching is: {course_name}."
    return titles_w_content_template(extra, prefix=prefix)


def lesson_template(lesson_name: str, **lesson_reqs) -> str:
    prompt = f"Today's lesson is: {lesson_name}.\n"
    return titles_w_content_template(lesson_reqs, prefix=prompt)


def slides_prompt_template(n_bullets: int = 4) -> str:
    return (
        slides_prompt
        + f"\nYou MUST give me at least {n_bullets} bullet points for per slide."
    )


def mcq_quiz_prompt_template(n_questions: int = 10) -> str:
    return mcq_prompt + f"\nYou MUST give me {n_questions} questions."
