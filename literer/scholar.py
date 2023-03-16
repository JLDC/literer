import requests
import warnings

# Semantic Scholar API urls
URL_KEYWORD = "https://api.semanticscholar.org/graph/v1/paper/search?"
URL_DETAILS = "https://api.semanticscholar.org/graph/v1/paper/"



def extract_paper_info(data):
    """
    Extract relevant information from a Semantic Scholar publication object.

    Args:
        - data (dict): A dictionary containing information on a single publication, including its
            title, authors, year, venue, abstract, citation styles, and tldr.

    Returns:
        - dict: A dictionary containing the title, authors, year, venue, abstract, citation styles,
            and tldr of the publication.
    """
    
    return {
        "title": data["title"],
        "authors": [a["name"] for a in data["authors"]],
        "year": data["year"],
        "venue": data["venue"],
        "abstract": data["abstract"],
        "bibtex": data["citationStyles"]["bibtex"],
        "summary": data["tldr"]
    }


def get_papers(
        keyword, npubs=30, year_start=None, year_end=None, venue=None,
        fields_of_study=None, publication_types=None):
    """
    Search for publications on Semantic Scholar using a keyword and optional filters.

    Args:
        - keyword (str): The keyword to search for in publication titles and abstracts.
        - npubs (int): The maximum number of publications to return. Defaults to 30.
        - year_start (int): The earliest year for which to retrieve publications.
        - year_end (int): The latest year for which to retrieve publications.
        - venue (str or list): The venue(s) where the publications were published.
        - fields_of_study (str or list): The field(s) of study related to the publications.
        - publication_types (str or list): The type(s) of publications to retrieve.

    Returns:
        - list: A list of dictionaries, where each dictionary contains information on a single publication.
            The dictionary includes keys for 'title', 'year', 'authors', 'venue', 'abstract',
            'bibtex', and 'tldr'.

    Examples:
        To search for publications related to machine learning published in 2021:
        >>> get_papers("machine learning", year_start=2021, year_end=2021, fields_of_study="Computer Science")
    """
    
    if npubs > 100:
        warnings.warn("The free API for Semantic Scholar cannot do more than " +
                      f"100 requests every 5 minutes. " +
                      f"Consider reducing 'npubs' (currently 'npubs' = {npubs}).")
    
    query = f"{URL_KEYWORD}query={keyword.replace(' ', '+')}&limit={npubs}"

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
        
    response = requests.get(query)
    publications = response.json()
    pub_list = []
    
    # Query relevant information for each publication
    for pub in publications["data"]:
        query = f"{URL_DETAILS}{pub['paperId']}"
        query += "?fields=year,authors,venue,abstract,citationStyles,tldr" 
        resp = requests.get(query)
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
    return '\n'.join([p["bibtex"] for p in publications])