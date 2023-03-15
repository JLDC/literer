import argparse
import openai
from scholarly import scholarly


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provide number of queries, publications, and topic")
    parser.add_argument("-t", "--topic")
    parser.add_argument("-q", "--queries", default=3)
    parser.add_argument("-p", "--publications", default=10)
    args = parser.parse_args()
    # Provide API key
    openai.api_key = open("api_key").readline()

    # Create the prompt to get Google Scholar prompts
    nprompts = args.queries # Number of prompts to suggest
    topic = args.topic
    prompt = "".join([
        f"Create a list of {nprompts} search queries to query Google Scholar ",
        f"and find top articles about {topic}. ",
        "Separate the search queries by | and do not use any quotes or new lines."])


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Clean response
    queries = [r.strip() for r in response["choices"][0]["message"]["content"].split("|")]

    # Print suggested queries
    print("Querying Google Scholar for: ")
    for q in queries:
        print(f"  - {q}")

    print("-" * 30)


    # Query Google Scholar
    npubs = args.publications # Number of first publications to check for each query
    all_text = []


    for i, q in enumerate(queries):
        pubs = []
        print(f"Searching Google Scholar for {q}... ", end="")
        results = scholarly.search_pubs(q)
        # Iterate over first npubs and store them
        for _ in range(npubs):
            pub = next(results)
            pubs.append(pub["bib"])
        print("creating review...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a research in causal econometrics."},
                {"role": "user", "content": f"Create a literature review from a short selection of the following publications only: {pubs}"}
            ]
        )
        all_text.append(response["choices"][0]["message"]["content"])
    print("-" * 30)
    print("\n".join(all_text))