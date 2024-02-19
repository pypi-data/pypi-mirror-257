from setuptools import setup, find_packages

setup(
    name="AudioUtils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
         'numpy', 'pydub', 'librosa', 'requests',
    ]
)