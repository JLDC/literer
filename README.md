# literer
**literer** is a Python package that combines the Semantic Scholar and OpenAI APIs to create a literature review on specified topics. The package allows users to specify keywords related to their research interest and generate a summary of relevant research papers.

## Installation
To install **literer**, you can use pip. Simply run the following command:

```
pip install literer
```

## Usage
After installation you can import the **literer** package and start using it.

```python
import literer as lit
import os

# Begin by setting API key
os.environ["OPENAI_KEY"] = "YOUR_API_KEY_HERE"

# Provide 5 keywords related to the chosen topic and that can be used to search semantic scholar
keywords = lit.get_keywords("neural networks for financial forecasting", nkeywords=5)



```

# Notes / Ideas
+ Custom ranking by GPT instead of Semantic Scholar
+ Use GPT to create the keywords

# TODOs
+ Fix bibtex, use regex to transform @None -> @article and stuff like @['JournalArticle']