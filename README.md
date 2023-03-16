# literer
**literer** is a Python package that combines the Semantic Scholar and OpenAI APIs to create a literature review on specified topics. The package allows users to specify keywords related to their research interest and generate a summary of relevant research papers.

## Installation
To install **literer**, clone this repository and install it in pip. Run the following commands:

```
git clone https://github.com/JLDC/literer   # Clone the repository
cd("literer")                               # Change the directory
pip install .                               # Install the package with pip
```

## Usage
After installation you can import the **literer** package and start using it.

```python
import literer as lit
import openai

# Get npubs=15 papers using a specific search keyword, one can also provide further
# filters, e.g., field of study, venue, or publication type (see docstring)
papers = lit.get_papers("deep learning for financial forecasting", npubs=15)

# Extract the BibTeX entries and save them to a bibliography.bib file
with open("bibiliography.bib", "w") as f:
    f.write(lit.create_bibliography(papers))

# Create literature review using TeX format (matches the bibliography defined above)
lit_review = lit.summarize_papers(papers, tex_format=True)
```

## Example review
> In recent years, there has been a growing interest in the application of deep learning techniques in financial forecasting. Geoghegan (2021) explores the use of meta-learning for financial market forecasting and proposes a meta-regularization approach to tackle the issue of meta-overfitting. Barra et al. (2020) demonstrate the potential of deep learning and time-series-to-image encoding for financial forecasting in a highly fluctuating market. Jin et al. (2022) introduce a deep learning model that utilizes empirical mode decomposition (EMD) with back-propagation neural networks (BPNN) for financial market forecasting, while Gao and Xia (2022) analyze the feasibility of applying recurrent neural networks for financial risk early warning of small and medium-sized board listed companies. 
> 
> Furthermore, Urbinate et al. (2022) highlight the importance of ensemble models' performance and combining each model's prediction for accurate forecasting, while Manjunath and Halasuru Manjunath (2022) propose a novel approach for forecasting financial markets using deep learning with long short-term networks. Khalil and Pipa (2021) emphasize the potential of deep-learning and natural language processing techniques in financial forecasting and investigate the impact of sentiments on stock direction. 
>
> Korczak and Hernes (2017) demonstrate the potential of deep learning models in financial time series forecasting in A-Trader system, and Persio and Honchar (2018) introduce a neural networks-based regularization approach to improve accuracy in cryptocurrency data forecasting. Additionally, Shuhidan et al. (2021) propose a stock price forecasting model based on sentiment analysis of financial news that leverages recurrent neural networks and long short-term memory networks. 
>
>Lin and Huang (2020) explore the use of deep learning and empirical mode decomposition for financial forecasting, while Bravo (2021) investigates the use of deep learning techniques to forecast longevity for financial applications. Finally, Deng and Yiu (2022) investigate the influences of financial news on stock trends from a deep multiple instance learning perspective, and Baldo et al. (2021) propose a new approach to forecasting financial time-series data using deep-learning and machine-learning tools. Ma and Ke (2021) present a multi-task learning framework for stock time-series forecasting that leverages information included in related stocks. Overall, this literature review highlights the potential of deep learning techniques to improve financial forecasting accuracy in various settings.



# Notes / Ideas
+ Custom ranking by GPT instead of Semantic Scholar?
+ Use GPT to create the keywords (-> actually turned out meh)

# TODOs
+ Fix bibtex, use regex to transform @None -> @article and stuff like @['JournalArticle']