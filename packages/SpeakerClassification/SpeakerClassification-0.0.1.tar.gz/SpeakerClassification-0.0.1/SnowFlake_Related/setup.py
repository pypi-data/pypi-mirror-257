from setuptools import setup, find_packages

setup(
    name="SnowFlake_Related",
    version="0.1",
    packages=find_packages(),
    install_requires=[
         'pandas', 'snowflake', 'sqlalchemy'
    ]
)