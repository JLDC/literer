import openai

def single_review(publication):
    prompt_system = ''.join(
        [
            "You are a researcher publishing in top journals. ",
            "You are currently writing a literature review for your upcoming research. ",
            "Make sure to properly cite the sources."
         ]
    )

    prompt_user = f"Create a brief review for {publication}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    )

    return response["choices"][0]["message"]["content"]


def full_review(publications):
    single_reviews = [single_review(pub) for pub in publications]

    prompt_system = ''.join(
        [
            "You are a researcher publishing in top journals. ",
            "You are currently writing a literature review for your upcoming research.",
            "Make sure to properly cite the sources."
         ]
    )

    prompt_user = f"Combine the following reviews for your literature review: \n\n{single_reviews}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]
    )

    return response["choices"][0]["message"]["content"]