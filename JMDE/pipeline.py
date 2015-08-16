from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def default():
    vectorizer  = ('vect',  CountVectorizer())
    transformer = ('tfidf', TfidfTransformer())
    classifier  = ('clf',   MultinomialNB())
    return Pipeline([vectorizer, transformer, classifier])
