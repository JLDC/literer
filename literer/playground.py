import literer as lit
import openai

# Begin by setting API key
openai.api_key = open("api_key").readline()

# Get npubs=15 papers using a specific search keyword, one can also provide further
# filters, e.g., field of study, venue, or publication type (see docstring)
papers = lit.get_papers("deep learning for financial forecasting", npubs=15)

# Extract the BibTeX entries and save them to a bibliography.bib file
with open("bibiliography.bib", "w") as f:
    f.write(lit.create_bibliography(papers))

# Create literature review using TeX format (matches the bibliography defined above)
lit_review = lit.summarize_papers(papers, tex_format=False)