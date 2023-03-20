import openai
import re
from typing import List

from .utils import get_content, get_openai_model, make_journal_string


def single_review(publication, topic, tex_format=False):
    """
    Generate a brief literature review for a given publication, using natural language prompts provided by OpenAI's GPT-3.

    Args:
        publication (dict): a dictionary containing information about a publication, including its title, authors, year, venue, abstract, and summary.
        tex_format (bool): whether to include TeX formatting in the output (default True).

    Returns:
        A string containing the review for the single paper.
    """

    # Drop bibtex key if not required to alleviate the number of tokens
    if not tex_format:
        del publication["bibtex"]

    messages = [
        {
        "role": "system",
        "content": ("You are a research assistant creating literature reviews "
                    "for your supervisor.")
        },
        {
        "role": "user",
        "content": (f"Create a brief review for {publication}.\n" 
                    "You want to use this review to write a paper on the topic "
                    f"of '{topic}' later on.")# TODO: TeX Format again?
        }
    ]
    response = openai.ChatCompletion.create(
        model=get_openai_model(),
        messages=messages
    )

    return get_content(response)

def summarize_papers(publications, topic, tex_format=False):
    """
    Generate a full literature review for a set of publications, each with their own brief review.

    Args:
        publications (list): A list of publications, where each publication is a dictionary with the following keys:
            - "title": the title of the publication
            - "authors": a list of authors for the publication
            - "year": the year the publication was published
            - "venue": the publication venue
            - "abstract": the abstract of the publication
            - "bibtex": the bibtex citation for the publication
            - "summary": a brief summary of the publication

        tex_format (bool): Whether or not to use TeX format for citations. Defaults to True.

    Returns:
        A string containing the full literature review.
    """
    # Drop any paper that do not have an abstract first
    publications = [p for p in publications if p["abstract"] != ""]
    single_reviews = [single_review(pub, topic, tex_format) for pub in publications]

    messages = [
        {
        "role": "system",
        "content": ("You are a research assistant creating literature reviews "
                    "for your supervisor.")
        },
        {
        "role": "user",
        "content": ("Combine the following reviews into a single literature "
                    f"review that focuses on the topic of '{topic}'. "
                    "Ensure that the reader understands why these papers are "
                    "relevant to the paper you are writing.\n"
                    '\n'.join(single_reviews))
        }
    ]
    response = openai.ChatCompletion.create(
        model=get_openai_model(),
        messages=messages
    )

    return get_content(response)

def get_keywords(topic: str, n_keywords: int) -> List[str]:
    """
    Provide search queries for finding literature relevant to a given topic on Semantic Scholar, 
    and returns a list of n_keywords keywords as provided by the user.

    Args:
        topic (str): The topic for which literature is to be searched.
        n_keywords (int): The number of keywords to request from the user.
        model (str, optional): The name of the OpenAI model to use for generating the prompt.
            Defaults to "gpt-4-0314".

    Returns:
        List[str]: A list of n_keywords keywords, as provided by the user and separated by '|'.
    """

    messages = [
        {
        "role": "system", 
        "content": ("You are a helpful research assistant that helps find "
                    "relevant literature online.")
        },
        {
        "role": "user", 
        "content": (f"Provide {n_keywords} queries to search for literature "
                    f"relevant to the topic of '{topic}' on Semantic Scholar. "
                    "Be aware that longer keywords will make it more difficult to find results. "
                    "Separate the search queries by '|', such that they are "
                    "easily parsable.")
        }
    ]

    response = openai.ChatCompletion.create(
        model=get_openai_model(),
        messages=messages
    )

    return [k.strip() for k in get_content(response).split("|")]

def judge_paper(publication, topic, target_journal):    
    if publication["abstract"] == "" or publication["abstract"] is None:
        return 0, "No abstract."
    
    journal_str = make_journal_string(target_journal)
    
    messages = [
        {
        "role": "system", 
        "content": ("You are a research assistant, you assess whether "
                    "publications are relevant to a given research topic.")
        },
        {
        "role": "user",
        "content": (f"You are writing a paper on the topic of {topic} and are "
                    f"aiming to publish to {journal_str}.\n"
                    "Is the following paper, published in the journal "
                    f"'{publication['venue']}' relevant to you?\n"
                    f"Abstract: {publication['abstract']}.\n"
                    "Give your answer in format RELEVANCE_SCORE|JUSTIFICATION " 
                    "where RELEVANCE_SCORE is an integer between 0 and 10 "
                    "and JUSTIFICATION is a brief reasoning of your score in "
                    "a maximum of 10 words.")
        }
    ]

    response = openai.ChatCompletion.create(
        model=get_openai_model(),
        messages=messages
    )

    score, reason = get_content(response).split("|")
    match = re.search(r'\d+', score)
    if match:
        score = int(match.group())

    return score, reason