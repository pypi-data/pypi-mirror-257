from ..utils import deindent


notes_prompt = deindent(
    """
    Please create comprehensive lecture notes that cover all key topics and subtopics about the upcoming lesson. The notes should include:
    - Detailed explanations of each subject area.
    - Definitions and clarifications of relevant terminology.
    - Practical examples and case studies where applicable.
    - Steps and strategies highlighting the instructional focus.
    - Summaries of theoretical frameworks or models introduced.
    - Interactive activity guidelines and expected learning outcomes.
    - Instructions for homework assignments and expected deliverables.
    - Additional resources for expanded learning on the lesson's topics.
    The notes should be organized in a clear, logical manner, suitable for academic use, and supportive of student comprehension and engagement. Make sure the content is appropriately sectioned for ease of reading and study, ready for print and distribution.
    Make sure the notesare enough for the whole duration of the lesson.
    """
)

slides_prompt = deindent(
    """
    I need detailed lecture slides with bullet points for the upcoming lesson. Include the approximate duration for each slide. Make sure they add up to the total lesson duration if mentioned above.
    The slides must strike a balance between engagement and informativeness, designed to facilitate independent learning for students.
    Aim for clarity without sacrificing accuracy or detail. Craft explanations, analogies, and examples with simplicity, ensuring students can grasp the content without the presence of a teacher.
    Please generate the actual content for each slide rather than just providing titles and guidelines. Something I can copy-paste directly.
    We can iterate on the slides together to refine and enhance them, so perfection is not necessary in the initial draft.
    Your goal is to make the material accessible and understandable to students studying independently.
    """
)

slides_format_prompt = deindent(
    """
    Take this material and convert it into a JSON with the following format:
    {"titles": ["title1", "title2", "title3"], "bullets": [["bullet1", "bullet2"], ["bullet1", "bullet2"], ["bullet1", "bullet2"]]})
    """
)

slides_notes_prompt = deindent(
    "Generate the instructor notes for the slides. These notes will have the complete extra detailed content for each slide."
)

mcq_scoring_prompt = "We will make a quiz for this lesson. Design a scoring guide that outlines the specific criteria for evaluating student responses. Assume all quiz questions are MCQs."

mcq_prompt = deindent(
    """
    You are designing a series of multiple-choice questions as a quiz for the lesson. Each question should test the students' knowledge, understanding, and ability to apply key concepts from the course material. Follow these guidelines:
    1. **Topic Focus**: Each question should be based on a major topic or sub-topic covered in the lesson.
    2. **Question Clarity**: Formulate each question clearly and concisely, ensuring that the central focus of the question is straightforward and unambiguous.
    3. **Distractors**: Provide 3-4 answer choices for every question. The incorrect choices (distractors) should be plausible and reflect common misconceptions or errors related to the topic to challenge students to think critically.
    4. **Complexity**: Design questions that require more than just recall of information. Include questions that test students' ability to analyze, synthesize, and evaluate information.
    5. **Variety**: Mix different types of questions, such as fact-based, scenario-based, and application-based questions, to cover various levels of Bloom’s Taxonomy.
    """
)

quiz_prompt = deindent(
    """
    Building on the lecture slides, I now need a short quiz to assess students' understanding of the material.
    Design a quiz that covers key concepts presented in the slides, ensuring a balance between challenging questions and those that reinforce fundamental knowledge.
    The quiz should reflect the simplicity and clarity of the lecture content. Each question should be accompanied by clear explanations of the correct answers to aid students in their learning process.
    Feel free to propose an initial draft of the quiz, and we can collaborate on refining it to ensure it aligns with the learning objectives of the lesson.
    The goal is to create an effective assessment tool that reinforces understanding and promotes active learning.
    """
)

quiz_format_prompt = deindent(
    """
    Reformat the quiz material into a JSON with the following format:
    {"questions": ["question1", "question2", "question3"], "answers": [["answer1", "answer2"], ["answer1", "answer2"], ["answer1", "answer2"]], "correct_indices": [0, 1, 0]}
    """
)
