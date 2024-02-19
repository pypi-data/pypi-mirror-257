from setuptools import setup, find_packages

setup(
    name="CallSummarization",
    version="0.1",
    packages=find_packages(),
    install_requires=['openai', 'pandas', 'langchain', 'tiktoken', 'nltk', 'tqdm',
                      'deep_translator', 'langchain-community', ]

)