import openai
from .utils import get_content

def single_review(publication, tex_format=True):
    """
    Generate a brief literature review for a given publication, using natural language prompts provided by OpenAI's GPT-3.

    Args:
        - publication (dict): a dictionary containing information about a publication, including its title, authors, year, venue, abstract, and summary.
        - tex_format (bool): whether to include TeX formatting in the output (default True).

    Returns:
        - A string containing the review for the single paper.
    """

    # Drop bibtex key if not required to alleviate the number of tokens
    if not tex_format:
        del publication["bibtex"]

    prompt_system = ''.join(
        [
            "You are a researcher publishing in top journals. ",
            "You are currently writing a literature review for your upcoming research. ",
            "Make sure to properly cite the sources",
            " using the proper TeX format." if tex_format else ""
         ]
    )

    prompt_user = ''.join(
        [
            f"Create a brief review for {publication}.",
            "\nMake sure to use the proper TeX format (\\textcite or \\parencite)." if tex_format else ""
        ]
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    )

    return get_content(response)

def full_review(publications, tex_format=True):
    """
    Generate a full literature review for a set of publications, each with their own brief review.

    Args:
        - publications (list): A list of publications, where each publication is a dictionary with the following keys:
            - "title": the title of the publication
            - "authors": a list of authors for the publication
            - "year": the year the publication was published
            - "venue": the publication venue
            - "abstract": the abstract of the publication
            - "bibtex": the bibtex citation for the publication
            - "summary": a brief summary of the publication

        - tex_format (bool): Whether or not to use TeX format for citations. Defaults to True.

    Returns:
        - A string containing the full literature review.
    """
    single_reviews = [single_review(pub, tex_format) for pub in publications]

    prompt_system = ''.join(
        [
            "You are a researcher publishing in top journals. ",
            "You are currently writing a literature review for your upcoming research.",
            "Make sure to properly cite the sources."
         ]
    )

    prompt_user = f"Combine the following reviews for your literature review: \n\n{single_reviews}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    )

    return get_content(response)




def get_keywords(topic, nkeywords=3):
    """
    Create a list of queries relevant to a given topic.

    Args:
        - topic (str): The topic to search for.
        - nkeywords (int, optional): The number of queries to create. Defaults to 3.

    Returns:
        - list: A list of `nkeywords` queries relevant to the given topic.

    Examples:
        To create 3 queries relevant to a topic:
        >>> get_keywords("machine learning")
        ["machine learning", "deep learning", "neural networks"]
        
        To create 5 queries relevant to a topic:
        >>> get_keywords("computer vision", nkeywords=5)
        ["object detection", "image segmentation", "optical flow", "convolutional neural networks", "feature extraction"]

    """
    prompt_system = "You are an assistant creating helpful queries to search relevant papers using the Semantic Scholar API."
    prompt_user = ''.join(
        [
            f"Create exactly '{nkeywords}' query keywords to search for papers relevant to '{topic}'. ",
            "Separate the search queries by | and do not use any quotes or newlines, e.g. 'query 1 | query 2 | ...'"
        ]
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    )

    queries = get_content(response)
    return [q.strip() for q in queries.split("|")]