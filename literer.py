import argparse
import openai

import review
import scholar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provide number of queries, publications, and topic")
    parser.add_argument("-t", "--topic")
    # parser.add_argument("-q", "--queries", default=3)
    parser.add_argument("-p", "--publications", default=20)
    args = parser.parse_args()
    # Provide API key
    openai.api_key = open("api_key").readline()

    # # Create the prompt to get Google Scholar prompts
    # nprompts = args.queries # Number of prompts to suggest
    # topic = args.topic
    # prompt = "".join([
    #     f"Create a list of {nprompts} search queries to query Google Scholar ",
    #     f"and find top articles about {topic}. ",
    #     "Separate the search queries by | and do not use any quotes or new lines."])


    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo", 
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )

    # Clean response
    # queries = [r.strip() for r in response["choices"][0]["message"]["content"].split("|")]

    # Search Semantic Scholar for publications
    print("Querying Semantic Scholar ...")
    print("-" * 50, end="\n\n")
    publications = scholar.search_by_keyword(args.topic, npubs=args.publications)


    # Create literature review
    print("Creating literature review (this might take a while) ...")
    print("-" * 50, end="\n\n")
    print(review.full_review(publications))