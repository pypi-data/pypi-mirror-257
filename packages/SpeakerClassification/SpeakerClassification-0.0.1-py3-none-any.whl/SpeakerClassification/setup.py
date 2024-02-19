from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SpeakerClassification",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'numpy', 'pandas', 'scikit-learn', 'nltk', 'boto3',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)