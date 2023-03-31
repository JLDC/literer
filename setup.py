from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="literer",
    version="0.1.4",
    license="MIT",
    description="literer is a package that combines the Semantic Scholar and OpenAI APIs to create automated literature reviews",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jonathan Chassot",
    author_email="jonathan.chassot@unisg.ch",
    url="https://github.com/JLDC/literer",
    keywords=["literature review", "openai", "semantic scholar"],
    install_requires=[
        "openai>=0.27.2",
        "requests>=2.28.2",
    ]
)
