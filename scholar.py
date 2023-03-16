import requests
import warnings

# Semantic Scholar API urls
URL_KEYWORD = "https://api.semanticscholar.org/graph/v1/paper/search?"
URL_DETAILS = "https://api.semanticscholar.org/graph/v1/paper/"


"""
Extracts relevant information from a dictionary / json returned by the Semantic Scholar API for a paper.

Parameters:
    data (dict): A dictionary / json representing a paper, as returned by the Semantic Scholar API.

Returns:
    dict: A dictionary with the following keys and values:
        - "title": the title of the paper (str).
        - "authors": a list of the names of the authors of the paper (list of str).
        - "year": the year the paper was published (int).
        - "venue": the venue where the paper was published (str).
        - "abstract": the abstract of the paper (str).
"""
def extract_paper_info(data):
    return {
        "title": data["title"],
        "authors": [a["name"] for a in data["authors"]],
        "year": data["year"],
        "venue": data["venue"],
        "abstract": data["abstract"]
    }


"""
Searches the Semantic Scholar API for publications that match a given keyword and optional filters, and extracts relevant information from each publication.

Parameters:
    keyword (str): A string representing the keyword to search for in the publication titles, abstracts or venues.
    npubs (int): The maximum number of publications to retrieve (default: 30).
    year_start (int): The start year of the publication range to retrieve (inclusive, default: None).
    year_end (int): The end year of the publication range to retrieve (inclusive, default: None).
    venue (str or list): A string or a list of strings representing the venues to search for (default: None).

Returns:
    list: A list of dictionaries representing the publications that match the search criteria, with the following keys and values:
        - "title": the title of the publication (str).
        - "authors": a list of the names of the authors of the publication (list of str).
        - "year": the year the publication was published (int).
        - "venue": the venue where the publication was published (str).
        - "abstract": the abstract of the publication (str).
"""

def search_by_keyword(keyword, npubs=30, year_start=None, year_end=None, venue=None):
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
            raise TypeError("'venue' must be a list or a string")
        
    response = requests.get(query)
    publications = response.json()
    pub_list = []
    
    # Query relevant information for each publication
    for pub in publications["data"]:
        query = f"{URL_DETAILS}{pub['paperId']}"
        query += "?fields=year,authors,venue,abstract" 
        resp = requests.get(query)
        data = resp.json()
        data["title"] = pub["title"]
        pub_list.append(extract_paper_info(data))

    return pub_list

