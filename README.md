# literer
**literer** is a Python package that combines the Semantic Scholar and OpenAI APIs to create a literature review on specified topics. The package allows users to specify keywords related to their research interest and generate a summary of relevant research papers.

## Installation
To install **literer**, install it using pip. Run the following commands:

```
pip install literer                               # Install the package with pip

# To uninstall the package again, just use
# pip uninstall literer
```

## Usage
After installation you can import the **literer** package and start using it.

### Configuring API keys and OpenAI Model
```python
import literer as lit
import openai

# Begin by setting OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"
# Optional: If you have one, you can also use your Semantic Scholar API key
s2_api_key = "YOUR_S2_API_KEY_HERE"
# Choose OpenAI model
lit.set_openai_model("gpt-4") # Default is 'gpt-3.5-turbo'
``` 

### Obtaining papers from Semantic Scholar

```python
# Get n_pubs=15 papers using a specific search keyword, one can also provide further
# filters, e.g., field of study, venue, or publication type (see docstring)
papers = lit.get_papers("active labor market policies", n_pubs=15,
    api_key=s2_api_key) # Leave api_key empty if you don't have one.

# Extract the BibTeX entries and save them to a bibliography.bib file
with open("bibiliography.bib", "w") as f:
    f.write(lit.create_bibliography(papers))
```

You can also ask **literer** to provide keywords to help you search for papers
```python
# Get 3 keywords suggestions
keywords = lit.get_keywords(topic="hetereogeneous treatment effects in active labor market policies", n_keywords=3)

# Iterate over the keywords and gather all papers into a larger list, filter
# to only return results from the top 5 econ journals
all_papers = []
for keyword in keywords:
    all_papers += get_papers(keyword=keyword, n_pubs=15, venue=lit.get_top_journals("Economics"))
```

### Provide a relevance score (and a reason for this score) based on the abstract
```python
scores, reasons = [], [] 

# Iterate over the collected paper, ask literer to provide a judgment of how
# relevant a given paper is based on a specific topic and a target journal for
# publication
topic = "heterogeneity of treatment effects in active labor market policies"
# target_journal can be either a list or a string of a single journal
target_journal = ["American Economic Review", "Quarterly Journal of Economics"]
for paper in papers:
    score, reason = lit.judge_paper(paper=paper, topic=topic, target_journal=target_journal)
    scores.append(score)
    reasons.append(reason)


# Optional: store the results in tabular form for ease of view
import pandas as pd

df_papers = pd.DataFrame({
    "authors": [", ".join(p["authors"]) for p in papers],
    "year": [p["year"] for p in all_papers],
    "title": [p["title"] for p in all_papers],
    "relevance_score": scores,
    "relevance_reason": reasons 
})
```

### Create a literature review to help you get a quick overview of the papers
```python
# Subset the papers to only keep the most relevant ones
min_relevance = 7 # Minimum relevance score to keep a paper in the literature review
best_papers = [p for i, p in enumerate(papers) if scores[i] >= min_relevance]
lit_review = lit.summarize_papers(best_papers)
```


## Example review

> Lechner (2002) emphasizes the importance of considering program heterogeneity when evaluating active labor market policies, particularly by comparing different propensity score techniques. This approach is also reflected in the study by Bennett and Ouazad (2018), which examines the impact of job displacement on crime rates and the mitigating role of active labor market policies in Denmark.
>
> Furthermore, studies by Sianesi (2004), Hoynes (1996), and Britto (2020) provide mixed evidence on the effectiveness of labor market interventions, highlighting the need for a delicate balance between financial support and activation measures for improving labor market outcomes. The role of unemployment benefits and short-time work programs in addressing different types of economic shocks is also underscored by Giupponi et al. (2022).
>
> On a global scale, the distinct challenges faced by developing countries, particularly in Africa, are explored by Bandiera et al. (2022), emphasizing the need for targeted policies that address the unique labor market obstacles faced by young African adults. Similarly, the challenges faced by specific populations, such as refugees and female workers, are analyzed by Brell et al. (2020) and Heath and Tan (2020), respectively, identifying the need for tailored interventions that empower these groups and promote their labor market integration.
>
> Lastly, the role of immigration restrictions as a form of active labor market policy is examined by Clemens et al. (2017), highlighting the limited and potentially perverse effects of such policies. This study underscores the importance of exploring a broader range of interventions and understanding their implications for labor market outcomes.
>
> Collectively, this literature provides a foundation for understanding the complexities of active labor market policies and their potential impacts on employment, wages, and welfare dependency. Future research should focus on disentangling the causal relationships between these policies and labor market outcomes, identifying optimal combinations of interventions, and understanding the long-term consequences of such policies on worker satisfaction and overall economic well-being.