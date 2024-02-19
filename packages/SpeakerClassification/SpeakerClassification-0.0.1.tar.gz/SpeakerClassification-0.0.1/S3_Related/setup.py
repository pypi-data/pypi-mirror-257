from setuptools import setup, find_packages

setup(
    name="S3_Related",
    version="0.1",
    packages=find_packages(),
    install_requires=[
         'boto3', 'pandas', 'os', 'json', 'botocore', 'tqdm', 'logging',
    ]
)