import numpy as np
import openai
import re
import tiktoken
from typing import List, Union

def get_content(openai_response):
    return openai_response.choices[0].message.content

def clean_bibtex(text: str) -> str:
    return re.sub(r'@[^{]*\{[^}]*\}', '@article{', text)

def make_journal_string(target_journal: Union[str, List[str]]) -> str:
    if type(target_journal) is str:
        journal_str = f"the following journal: '{target_journal}'"
    elif type(target_journal) is list:
        target_journal = "'" + "', '".join(target_journal) + "'"
        journal_str = f"one of the following journals: {target_journal}"
    else:
        raise TypeError("'target_journal' must be either a str or list")
    
    return journal_str

OPENAI_MODEL = "gpt-3.5-turbo"

def get_openai_model():
    global OPENAI_MODEL
    return OPENAI_MODEL

def set_openai_model(new_model: str):
    """
    Set the value of the global variable OPENAI_MODEL to the given new_model.

    Args:
        new_model (str): The new value to set OPENAI_MODEL to.

    Returns:
        None.

    Example:
        >>> set_openai_model("gpt3")
        >>> summarize_papers(...)
        "Papers summarized using gpt3 model."
    """
    if new_model not in [m["id"] for m in openai.Model.list()["data"]]:
        raise ValueError((f"{new_model} is not a valid openai model or the API "
                          "key provided does not have access to it."))
    global OPENAI_MODEL 
    OPENAI_MODEL = new_model


def count_tokens(input: str, model: str) -> int:
    """
    Count the number of tokens in the given input using the given model.
    
    Args:
        input (str): The input text to count the number of tokens for.
        model (str): The model to use to count the number of tokens.
        
    Returns:
        int: The number of tokens in the given input.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(input))

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

def break_into_tokens(input: str, n_tokens: int, model: str) -> List[str]:
    """
    Break the given input into tokens using the given model.
    
    Args:
        input (str): The input text to break into tokens.
        n_tokens (int): The number of tokens to break the input into.
        model (str): The model to use to break the input into tokens.
        
    Returns:
        List[str]: A list of tokens that make up the given input.
    """
    # Break down into paragraphs
    paragraphs = make_paragraphs(input)
    text = []
    # Count number of token per paragraph
    encoding = tiktoken.encoding_for_model(model)
    tokens = np.cumsum([len(encoding.encode(p)) for p in paragraphs])
    # Calculate a rough split of the input into n_tokens
    rough_split = tokens[-1] // n_tokens + 1
    past_i = 0
    splits = 0
    for (i, e) in enumerate(tokens):
        if e > n_tokens * (splits + 1):
            if i == 0:
                raise ValueError(
                    "The first paragraph is too long to be tokenized.")
            text.append(''.join(paragraphs[past_i:i]))
            past_i = i
            splits += 1
        elif i == len(tokens) - 1:
            text.append(''.join(paragraphs[past_i:]))
    return text