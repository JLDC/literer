import re

def get_content(openai_response):
    return openai_response.choices[0].message.content

def clean_bibtex(text):
    return re.sub(r'@[^{]*\{[^}]*\}', '@article{', text)