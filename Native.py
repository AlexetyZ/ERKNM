import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os
import pickle
from sklearn.naive_bayes import MultinomialNB
from Dictionary import typicalReasons


VECTORIZER_FILENAME = 'vectorizer.pkl'
CLASSIFIER_FILENAME = 'classifier.pkl'

def tokenize_comment(comment):
    tokens = word_tokenize(comment)
    # Лемматизация слов
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmas


def train_tfidf_model(comments):
    vectorizer = TfidfVectorizer(tokenizer=tokenize_comment, strip_accents='unicode', )
    tfidf_matrix = vectorizer.fit_transform(comments)
    with open(VECTORIZER_FILENAME, 'wb') as f:
        pickle.dump(vectorizer, f)
    return vectorizer, tfidf_matrix


def update_classifier():
    if os.path.exists(VECTORIZER_FILENAME):
        # with open(VECTORIZER_FILENAME, 'rb') as vectorFile:
        #     vectorizer = pickle.load(vectorFile)
        comment = 'В разделе «Обязательные требования» включены структурные единицы НПА, не входящие в перечень НПА, содержащих обязательные требования, оценка соблюдения которых осуществляется в рамках данного вида контроля (надзора).'

        vectorizer = CountVectorizer(tokenizer=tokenize_comment)
        X = vectorizer.fit_transform([comment])
        if os.path.exists(CLASSIFIER_FILENAME):
            with open(CLASSIFIER_FILENAME, 'rb') as classFile:
                classifier = pickle.load(classFile)
        else:
            classifier = MultinomialNB()
        classifier.fit(X, typicalReasons)
        with open(CLASSIFIER_FILENAME, 'wb') as classFile:
            pickle.dump(classifier, classFile)

def createClassifierVertor(comment):
    vectorizer = CountVectorizer(tokenizer=tokenize_comment)
    X = vectorizer.fit_transform([comment])
    classifier = MultinomialNB()
    classifier.fit(X, typicalReasons)

def get_keyphrases(comment, vectorizer, tfidf_matrix):
    comment_tfidf = vectorizer.transform([comment])
    feature_names = vectorizer.get_feature_names()
    sorted_indices = comment_tfidf.toarray().argsort()[0][::-1]
    keyphrases = [feature_names[idx] for idx in sorted_indices[:5]]  # получить 5 наиболее значимых слов
    return keyphrases

class Vector:
    def __init__(self):

        if os.path.exists(VECTORIZER_FILENAME):
            with open(VECTORIZER_FILENAME, 'rb') as f:
                self.vectorizer = pickle.load(f)
        else:
            self.vectorizer = TfidfVectorizer(tokenizer=tokenize_comment)

    def get_keyphrases(self, comment):
        comment_tfidf = self.vectorizer.transform([comment])
        feature_names = self.vectorizer.get_feature_names_out()
        sorted_indices = comment_tfidf.toarray().argsort()[0][::-1]
        keyphrases = [feature_names[idx] for idx in sorted_indices[:5]]  # получить 5 наиболее значимых слов
        return keyphrases

    def classify_comments(self, comments, vectorizer, classifier):
        X = vectorizer.transform(comments)
        predicted_labels = classifier.predict(X)
        return predicted_labels


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression





if __name__ == '__main__':

    comment = 'В разделе «Обязательные требования» включены структурные единицы НПА, не входящие в перечень НПА, содержащих обязательные требования, оценка соблюдения которых осуществляется в рамках данного вида контроля (надзора).'

    # print(train_tfidf_model(typicalReasons))

    print(Vector().get_keyphrases(comment))
    # CommentClassifier().predict(comment)
