import re
import string
import time
from tokenize import tokenize

import nltk
from collections import Counter

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from textstat import textstat

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

from sklearn.neighbors import KNeighborsClassifier, KernelDensity
from sklearn.metrics import accuracy_score, balanced_accuracy_score
import pyphen
import numpy as np
import pandas as pd
from nltk.corpus import wordnet, stopwords
from dale_chall import DALE_CHALL
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

"""Citirea datelor in dataframe"""

loc = './data/'

dtypes = {"sentence": "string", "token": "string", "complexity": "float64"}
train = pd.read_excel(loc + 'train.xlsx', dtype=dtypes, keep_default_na=False)
test = pd.read_excel(loc + 'test.xlsx', dtype=dtypes, keep_default_na=False)

train.head()

def corpus_feature(corpus):
  if corpus =='bible':
    return [0]
  elif corpus =='biomed':
    return [1]
  else:
    return [2]


def nr_vowels(word):
  c = 0
  for i in word:
    if i in "aeiouAEIOU":
      c += 1
  return c

def is_dale_chall(word):
  return int(word.lower() in DALE_CHALL)

def is_title(word):
  return int(word.istitle())

def nr_syllables(word):
  language = pyphen.Pyphen(lang='en')
  x = language.inserted(word, '-').split('-')
  return len(x)

def filter_sentence(df):
    sw = set(stopwords.words('english'))
    cleaned_sentences = []
    for index, row in df.iterrows():
        wordtokens = word_tokenize(row['sentence'])
        filtered = []
        for word in wordtokens:
            if word not in '''!()-[]{};:'"\,<>./?@#$%^&*_~''``''':
                if word not in sw :
                  filtered.append(word)
        cleaned_sentences.append(" ".join(filtered))
    df['cleaned_sentence'] = cleaned_sentences
    return df

def vectorize_sentences(df, corpus):
    vectorizer = CountVectorizer()
    vectorized_corpus = vectorizer.fit_transform(df[corpus])
    #print(vectorizer.get_feature_names())
    df['vectorized_cleaned_sentence'] = vectorized_corpus.toarray().tolist()
    return df


def get_word_structure_features(word):
    features = []
    #features.append(frecventa(word))
    features.append(nr_syllables(word))
    features.append(is_dale_chall(word))
    features.append(len(word))
    features.append(nr_vowels(word))
    features.append(is_title(word))
    return np.array(features)


def synsets(word):
  return len(wordnet.synsets(word))


def get_wordnet_features(word):
  features = []
  features.append(synsets(word))
  return np.array(features)

def get_readibilty_of_sentence(profile_text):
    return[textstat.difficult_words(profile_text),
           textstat.gunning_fog(profile_text)]


def featurize(row):
    word = row['token']
    all_features = []
    all_features.extend(corpus_feature(row['corpus']))
    all_features.extend(get_word_structure_features(word))
    all_features.extend(get_wordnet_features(word))
    all_features.extend(get_readibilty_of_sentence(row['sentence']))
#    all_features.extend(row['vectorized_cleaned_sentence'])
    return np.array(all_features)

def featurize_df(df):
    nr_of_features = len(featurize(df.iloc[0]))
    nr_of_examples = len(df)
    global all_words
    features = np.zeros((nr_of_examples, nr_of_features))
    for index, row in df.iterrows():
        row_ftrs = featurize(row)
        features[index, :] = row_ftrs
    return features

current = time.time()
X_train_compr, X_test_compr, y_train_compr, y_test_compr = train_test_split(train[['corpus','sentence','token']], train['complex'],
                                                                            test_size=0.20, stratify=train['complex'])
X_train_compr = X_train_compr.reset_index(drop=True)
X_test_compr = X_test_compr.reset_index(drop=True)
y_train_compr = y_train_compr.reset_index(drop=True)
y_test_compr = y_test_compr.reset_index(drop=True)

X_train = featurize_df(X_train_compr)
X_test = featurize_df(X_test_compr)


model = GaussianNB()
model.fit(X_train, pd.Series(y_train_compr))
preds = model.predict(X_test)

# grid_params = { 'n_neighbors' : [5,7,9,11,13,15],
#                'weights' : ['uniform','distance'],
#                'metric' : ['minkowski','euclidean','manhattan']}
#
# gs = GridSearchCV(KNeighborsClassifier(), grid_params, verbose = 1, cv=3, n_jobs = -1)
#
# #Print The value of best Hyperparameters
# gs.fit(X_train, y_train_compr.values)
# print(gs.best_params_)

# model = KNeighborsClassifier(n_neighbors=13, weights='uniform', metric='manhattan')
# model.fit(X_train, y_train_compr.values)
# preds = model.predict(X_test)

print(time.time() - current)

print(balanced_accuracy_score(pd.Series(y_test_compr), preds))

test = filter_sentence(test)
X_test = featurize_df(test)
preds = model.predict(X_test)

df = pd.DataFrame()
df['id'] = test.index + len(train) + 1
df['complex'] = preds
df.to_csv('submission.csv', index=False)