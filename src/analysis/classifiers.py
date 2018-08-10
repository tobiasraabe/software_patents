#!/usr/bin/env python

"""This module contains pipelines to build prediction models.

"""
from sklearn.decomposition import PCA

# fmt: off
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectFromModel, SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from src.analysis.auxiliary import identity
from src.analysis.transformers import NLTKPreprocessor

# This is the original classifier used in the thesis
OriginalClassifier = Pipeline([
    ('vectorizer', CountVectorizer(max_df=0.7, ngram_range=(1, 4),
                                   analyzer='word')),
    ('feature_selection', SelectKBest(chi2, k=200)),
    ('classifier', RandomForestClassifier(n_estimators=5000,
                                          criterion='gini',
                                          max_features=0.3, n_jobs=-1)),
])


# This section includes models to improve the model selection process in
# this thesis. The first model should be very basic and serve a bottom line.
# After that, one iterates over each part of the pipeline to achieve more
# power.

####################################
#                                  #
#  Models based on numerical data  #
#                                  #
####################################

# This section contains prediction models which only handle numerical data. The
# models should use the same data as Bessen & Hunt (2007) but outperform their
# algorithm's results.

# 1. Logit
Logit = Pipeline([
    ('pca', PCA(n_components=None)),
    ('classifier', LogisticRegression()),
])


#############################
#                           #
# Models based on text data #
#                           #
#############################

# This section contains prediction models which work with text data in contrast
# to the classifiers based on numerical data. This additional analysis will
# show whether analyzing the complete patent text can improve the performance
# over the keyword methods by Bessen & Hunt (2007).

# This is an arbitrary better classifier
ImprovedClassifier = Pipeline([
    ('preprocessor', NLTKPreprocessor()),
    ('vectorizer', TfidfVectorizer(
        tokenizer=identity, preprocessor=None, lowercase=False,
        ngram_range=(1, 4), min_df=0.05
    )),
    ('feature_selection', SelectFromModel(
        RandomForestClassifier(n_jobs=3), threshold='mean')),
    ('classifier', ExtraTreesClassifier(
        n_estimators=1000, max_features=0.3, n_jobs=3)),
])
