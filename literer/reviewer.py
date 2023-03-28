import openai
import tiktoken
from typing import List, Tuple, Union

from .utils import get_content, get_openai_model, make_journal_string, break_into_tokens

def make_paragraphs(text: str, splitter: str ="\n\n") -> List[str]:
    """
    Split the given text into a list of paragraphs using the specified splitter.

    Args:
        text (str): The input text to split into paragraphs.
        splitter (str, optional): The string that marks the end of a paragraph. Defaults to "\n\n".

    Returns:
        List[str]: A list of strings representing the individual paragraphs of the input text.

    Example:
        >>> text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nAnd this is the third."
        >>> make_paragraphs(text)
        ['This is the first paragraph.', 'This is the second paragraph.', 'And this is the third.']
    """
    return text.split(splitter)

def give_feedback(
        excerpt: str, target_journal: Union[str, List[str]], 
        input_tokens: int = 4000
        ) -> Tuple[List[str], List[str]]:
    journal_str = make_journal_string(target_journal)
    
    # Break the excerpt into tokens of length input_tokens
    paragraphs = break_into_tokens(excerpt, input_tokens, get_openai_model())
    responses = []

    for paragraph in paragraphs:
        messages=[
            {
            "role": "system", "content": "You are the journal editor.",
            },
            {
            "role": "user", 
            "content": (
                f"A researcher is aiming to publish to {journal_str}. "
                "Provide feedback on his work. "
                "Be concise and specific, provide ideas and examples where "
                f"needed on how to improve his following research:\n{paragraph}")
            }
        ]
        response = openai.ChatCompletion.create(
            model=get_openai_model(),
            messages=messages
        )
        responses.append(get_content(response))
    
    return paragraphs, responses

def incorporate_feedback(
        excerpt: List[str], feedback: List[str], target_journal: Union[str, List[str]], 
        ) -> str:
    """
    Incorporate feedback into the given excerpt.

    Args:
        excerpt (str): The excerpt to incorporate feedback into.
        feedback (str): The feedback to incorporate into the excerpt.

    Returns:
        str: The excerpt with the feedback incorporated into it.
    """
    journal_str = make_journal_string(target_journal)
    responses = []
    for e, f in zip(excerpt, feedback):
        messages=[
            {
            "role": "system", "content": "You are an academic researcher.",
            },
            {
            "role": "user", 
            "content": (
                "Please help me incorporate the following feedback from the "
                "journal editor into the given excerpt from the researcher's "
                f"submission to {journal_str}. \n\nExcerpt:\n"
                f"`{e}`\n\nFeedback:\n`{f}`\n\n"
                "Incorporate the feedback and improve the excerpt based on the "
                "suggestions provided. Only answer witht the improved excerpt.")
            },
        ]

        response = openai.ChatCompletion.create(
            model=get_openai_model(),
            messages=messages
        )
        responses.append(get_content(response))
    return responses