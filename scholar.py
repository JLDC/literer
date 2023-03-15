from scholarly import scholarly

# Extract relevant information in dictionary format from a publication object
# using bibtex=true helps build the bibliography but slows down the process by a lot
def extract_info(pub, bibtex=True):
    info = {
        "title": pub["bib"]["title"],
        "author": pub["bib"]["author"],
        "year": pub["bib"]["pub_year"],
        "journal": pub["bib"]["venue"],
        "cited_by": pub["num_citations"],
        "abstract": pub["bib"]["abstract"]
    }
    if bibtex:
        info["bibtex"] = scholarly.bibtex(pub)
    return info

# Return a list of dictionaries with the information for the first `npubs`` given `keywords`
def get_publications(keywords, npubs=30, bibtex=True):
    pubs = scholarly.search_pubs(keywords)
    return [extract_info(next(pubs), bibtex) for _ in range(npubs)]



all_pubs = get_publications("method of simulated moments", npubs=5, bibtex=False)
all_pubs[1]['abstract']

pub = next(pubs)

btx = scholarly.bibtex(pub)