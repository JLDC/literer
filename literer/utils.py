def get_content(openai_response):
    return openai_response.choices[0].message.content