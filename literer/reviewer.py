import openai
from typing import List, Union

from .utils import get_content, get_gpt_model, make_journal_string

def give_feedback(paragraph: str, target_journal: Union[str, List[str]]) -> str:
    journal_str = make_journal_string(target_journal)
    messages=[
        {
        "role": "system", "content": "You are a strict academic reviewer.",
        },
        {
        "role": "user", 
        "content": (f"A researcher is aiming to publish to {journal_str}. "
                    f"Provide strict feedback on this excerpt:\n{paragraph}")
        }
    ]

    response = openai.ChatCompletion.create(
        model=get_gpt_model(),
        messages=messages
    )
    
    return get_content(response)


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

