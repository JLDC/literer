import re
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

GPT_MODEL = "gpt-4"

def get_gpt_model():
    global GPT_MODEL
    return GPT_MODEL

def set_gpt_model(new_model: str):
    """
    Set the value of the global variable GPT_MODEL to the given new_model.

    Args:
        new_model (str): The new value to set GPT_MODEL to.

    Returns:
        None.

    Example:
        >>> set_gpt_model("gpt3")
        >>> summarize_papers(...)
        "Papers summarized using gpt3 model."
    """
    if new_model not in [m["id"] for m in openai.Model.list()["data"]]:
        raise ValueError((f"{new_model} is not a valid openai model or the API "
                          "key provided does not have access to it."))
    global GPT_MODEL 
    GPT_MODEL = new_model