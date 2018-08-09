import string

from sklearn.base import BaseEstimator, TransformerMixin

from nltk import WordNetLemmatizer, pos_tag, sent_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords as sw, wordnet as wn


class NLTKPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True):
        self.lower = lower
        self.strip = strip
        self.stopwords = stopwords or set(sw.words('english'))
        self.punct = punct or set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

    def fit(self, X, y=None):
        return self

    def inverse_transform(self, X):
        return [" ".join(doc) for doc in X]

    def transform(self, X):
        return [list(self.tokenize(doc)) for doc in X]

    def tokenize(self, document):
        # Break the document into sentences
        for sent in sent_tokenize(document):
            # Break the sentence into part of speech tagged tokens
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                # Apply preprocessing to the token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token

                # If stopword, ignore token and continue
                if token in self.stopwords:
                    continue

                # If punctuation, ignore token and continue
                if all(char in self.punct for char in token):
                    continue

                # If token number, ignore and continue
                try:
                    int(token)
                except ValueError:
                    pass
                else:
                    continue
                # If token contains fig, ignore and continue
                if 'fig' in token:
                    continue

                # If token has length one, ignore and continue
                if len(token) == 1:
                    continue

                # Lemmatize the token and yield
                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {'N': wn.NOUN, 'V': wn.VERB, 'R': wn.ADV, 'J': wn.ADJ}.get(
            tag[0], wn.NOUN
        )

        return self.lemmatizer.lemmatize(token, tag)
