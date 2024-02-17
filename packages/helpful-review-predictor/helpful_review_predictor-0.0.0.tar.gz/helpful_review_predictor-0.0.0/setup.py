from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'Predicting helpfulness of reviews'
LONG_DESCRIPTION = 'A package that predicts the helpfulness of reviews using machine learning.'

# Setting up
setup(
    name="helpful_review_predictor",
    author="Mojtaba Maleki",
    author_email="<mojtaba.maleki.138022@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scikit-learn', 'numpy', 'scipy', 'joblib', 'textblob'],
    keywords=['python', 'webdevelopment', 'amazon', 'ecommerce', 'online shop', 'review', 'comment','machine learning', 'review analysis', 'helpful review predictor'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
