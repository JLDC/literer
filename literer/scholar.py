import requests
from typing import List
import warnings
from .utils import clean_bibtex

# Semantic Scholar API urls
URL_KEYWORD = "https://api.semanticscholar.org/graph/v1/paper/search?"
URL_DETAILS = "https://api.semanticscholar.org/graph/v1/paper/"

def extract_paper_info(data):
    """
    Extract relevant information from a Semantic Scholar publication object.

    Args:
        - data (dict): A dictionary containing information on a single publication, including its
            title, authors, year, venue, abstract, and citation styles.

    Returns:
        - dict: A dictionary containing the title, authors, year, venue, abstract, and 
            bibtex entry of the publication.
    """
    
    return {
        "title": data["title"],
        "authors": [a["name"] for a in data["authors"]],
        "year": data["year"],
        "venue": data["venue"],
        "abstract": data["abstract"],
        "bibtex": data["citationStyles"]["bibtex"],
        "url": data["url"]
    }


def get_papers(
        keyword, n_pubs=30, year_start=None, year_end=None, venue=None,
        fields_of_study=None, publication_types=None, api_key=None):
    """
    Search for publications on Semantic Scholar using a keyword and optional filters.

    Args:
        - keyword (str): The keyword to search for in publication titles and abstracts.
        - n_pubs (int): The maximum number of publications to return. Defaults to 30.
        - year_start (int): The earliest year for which to retrieve publications.
        - year_end (int): The latest year for which to retrieve publications.
        - venue (str or list): The venue(s) where the publications were published.
        - fields_of_study (str or list): The field(s) of study related to the publications.
        - publication_types (str or list): The type(s) of publications to retrieve.
        - api_key (str): Semantic scholar API key

    Returns:
        - list: A list of dictionaries, where each dictionary contains information on a single publication.
            The dictionary includes keys for 'title', 'year', 'authors', 'venue', 'abstract', and 'bibtex'.

    Examples:
        To search for publications related to machine learning published in 2021:
        >>> get_papers("machine learning", year_start=2021, year_end=2021, fields_of_study="Computer Science")
    """
    
    if n_pubs > 100:
        warnings.warn("The free API for Semantic Scholar cannot do more than " +
                      f"100 requests at once, n_pubs has been set to 100.")
        n_pubs = 100
    
    query = f"{URL_KEYWORD}query={keyword.replace(' ', '+')}&limit={n_pubs}"
    # Set API key if we have it
    if api_key is not None:
        headers = {"x-api-key": api_key}
    else:
        headers = None

    # Restrict results to a given year range
    if year_start is None:
        year_start = ""
    if year_end is None:
        year_end = ""

    if year_end == year_start:
        year_range = year_start
    else:
        year_range = f"{year_start}-{year_end}"

    if len(year_range):
        query += f"&year={year_range}"

    # Filter venues (can be a list or string of a single venue)
    if venue is not None:
        if type(venue) is str:
            query += f"&venue={venue}"
        elif type(venue) is list:
            query += f"&venue={','.join(venue)}"
        else:
            raise TypeError("'venue' must be a list or a str")
        
    if fields_of_study is not None:
        if type(fields_of_study) is str:
            fields_of_study = [fields_of_study]
        if type(fields_of_study) is list:
            # Make sure fields_of_study are valid
            map(check_field_of_study_validity, fields_of_study)
            query += f"&fieldsOfStudy={','.join(fields_of_study)}"
        else:
            raise TypeError("'fields_of_study' must be a list or str")
    
    if publication_types is not None:
        if type(publication_types) is str:
            publication_types = [publication_types]
        if type(publication_types) is list:
            # Make sure publication types are valid
            map(check_publication_type_validity, publication_types)
            query += f"&publicationType={','.join(publication_types)}"
        else:
            raise TypeError("'publication_types' must be a list or str")
        
    response = requests.get(query, headers=headers)
    warn_error(response)
    publications = response.json()
    pub_list = []

    # Special case when there are no publications found.
    if publications["total"] == 0:
        return pub_list
    # Query relevant information for each publication
    for pub in publications["data"]:
        query = f"{URL_DETAILS}{pub['paperId']}"
        query += "?fields=year,authors,venue,abstract,citationStyles,url" 
        resp = requests.get(query, headers=headers)
        warn_error(resp)
        data = resp.json()
        data["title"] = pub["title"]
        pub_list.append(extract_paper_info(data))
    return pub_list



ALL_PUBLICATION_TYPES = [
    "Review",
    "JournalArticle",
    "CaseReport",
    "ClinicalTrial",
    "Dataset",
    "Editorial",
    "LettersAndComments",
    "MetaAnalysis",
    "News",
    "Study",
    "Book",
    "BookSection"
]

ALL_FIELDS_OF_STUDY = [
    "Computer Science",
    "Medicine",
    "Chemistry",
    "Biology",
    "Materials Science",
    "Physics",
    "Geology",
    "Psychology",
    "Art",
    "History",
    "Geography",
    "Sociology",
    "Business",
    "Political Science",
    "Economics",
    "Philosophy",
    "Mathematics",
    "Engineering",
    "Environmental Science",
    "Agricultural and Food Sciences",
    "Education",
    "Law",
    "Linguistics"
]


def check_field_of_study_validity(field_of_study):
    if field_of_study not in ALL_FIELDS_OF_STUDY:
        raise ValueError(f"'{field_of_study}' is not a valid field of study.")

def check_publication_type_validity(publication_type):
    if publication_type not in ALL_PUBLICATION_TYPES:
        raise ValueError(f"'{publication_type}' is not a valid publication type.")

def create_bibliography(publications):
    """
    Generates a bibliography in BibTeX format from a list of publications.

    Args:
        - publications (list): A list of dictionaries, where each dictionary represents a publication
            and has a "bibtex" key with the BibTeX entry for that publication.

    Returns:
        - str: A string representing the concatenated BibTeX entries of all publications in the list,
        separated by newline characters.
    """
    return '\n'.join([clean_bibtex(p["bibtex"]) for p in publications])

def warn_error(response):
    if response.status_code != 200:
        warnings.warn(f"Semantic Scholar error encountered: \n\t{response.json()['error']}")

def get_top_journals(field: str, top5: bool =True) -> List[str]:
    if field not in TOP_JOURNALS:
        raise KeyError("Top journals for this field have not been compiled yet.")
    if top5:
        return TOP_JOURNALS[field][:5]
    else:
        return TOP_JOURNALS[field]

# Top 5 are top 5, rest is simply good
TOP_JOURNALS = {
    "Economics": [
        "American Economic Review",
        "Econometrica",
        "Journal of Political Economy",
        "Quarterly Journal of Economics",
        "Review of Economic Studies",
        
        "Economic Journal",
        "European Economic Review",
        "Journal of the European Economic Association",
        "Review of Economic Studies",
        "Review of Economics and Statistics",
        "Annual Review of Economics",
        "Journal of Economic Literature",
        "Journal of Economic Perspectives",
    ],

    "Finance": [
        "Journal of Finance",
        "Journal of Financial Economics",
        "Review of Financial Studies",
        "Journal of Financial and Quantitative Analysis",
        "Journal of Accounting and Economics",

        "Journal of Banking and Finance",
        "Quantitative Finance"
    ]
}