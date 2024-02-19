# setup.py

from setuptools import setup

setup(
    name='samplelib2',
    version='0.0.2',
    packages=['samplelib2'],
    install_requires=[
        "samplelib1"
    ],
)