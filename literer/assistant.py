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

def summarize_papers(publications, tex_format=True):
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