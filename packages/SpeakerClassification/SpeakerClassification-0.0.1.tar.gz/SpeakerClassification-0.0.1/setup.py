from setuptools import setup, find_packages
import CallSummarisation
import SpeakerClassification
import TextUtils
import AudioUtils

setup(
    name="JarvisMLMachineLearningHelper",
    version="0.1",
    packages=[
        'CallSummarisation',
        'SpeakerClassification',
        'TextUtils',
        'AudioUtils',

    ],
    install_requires=[
         'boto3' ,
    ]
)