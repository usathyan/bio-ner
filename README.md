#Introduction

This is a sample program to use the sciSpaCy models against biological documents to extract the various entities from it.
This will be useful to generate knowledge graphs from unstructured data
This file can read any document supported by Microsoft's markitdown library -DOC, DOCX, CSV, XLS, PPT, PDF, ZIP etc.
It then uses 4 different models to extract various entities from it. See file entities.txt for a sample output against FOXA1.txt (a saved abstract from PubMed. 

## Notes
The way to install packages for me were:
'''
python -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz

'''
That should download and install the necessary packages for the project.

For more details refer here - https://github.com/allenai/scispacy?tab=readme-ov-file
