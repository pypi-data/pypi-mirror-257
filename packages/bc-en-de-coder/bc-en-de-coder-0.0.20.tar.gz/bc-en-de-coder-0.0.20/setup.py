from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.20'
DESCRIPTION = 'Data Protecting Package'
LONG_DESCRIPTION = 'This package helps to protect all the data which you pass to LLM by encoding it first and decoding it afterward.'
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# Setting up
setup(
    name="bc-en-de-coder",
    version=VERSION,
    author="Abhishek Kumar Singh",
    author_email="<abhishek123kumar123singh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['bc_endecoder'],
    url='https://github.com/Distructor2404/bc-en-de-coder',
    install_requires=['PyPDF2', 'pandas','openpyxl'],
    keywords=['python', 'Data secure', 'Encoder', 'Decoder', 'pdf reader'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)