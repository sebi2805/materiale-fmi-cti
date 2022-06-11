import re
import time

import nltk
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, KFold
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from wordfreq import word_frequency
from textstat import textstat
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
import pyphen
import numpy as np
import pandas as pd
from nltk.corpus import wordnet, stopwords
from dale_chall import DALE_CHALL
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

"""Citirea datelor in dataframe"""

loc = './data/'

dtypes = {"sentence": "string", "token": "string", "complexity": "float64"}
train = pd.read_excel(loc + 'train.xlsx', dtype=dtypes, keep_default_na=False)
test = pd.read_excel(loc + 'test.xlsx', dtype=dtypes, keep_default_na=False)

train.head()

def preprocess(corpus):
    for text in corpus:
        text = text.lower()
        text = [re.sub("[^A-Za-z']+", ' ', word) for word in text.split(' ')]
        text = ' '.join(text)
        text = text.strip()

    return corpus

def get_idf_train(corpus):
    corpus = preprocess(corpus)
    stop_list = set(stopwords.words('english'))
    vectorizer = TfidfVectorizer(use_idf=True, stop_words=set(stop_list))
    tfidf_train = vectorizer.fit_transform(corpus)
    idf = vectorizer.idf_
    return vectorizer, dict(zip(vectorizer.get_feature_names(), idf))

def get_idf_test(vectorizer, corpus):
    corpus = preprocess(corpus)
    stop_list = set(stopwords.words('english'))
    tfidf_train = vectorizer.transform(corpus)
    idf = vectorizer.idf_
    return dict(zip(vectorizer.get_feature_names(), idf))

def get_idf_score(dictionary, word):
    value = dictionary.get(word)
    if value:
        return [value]
    else:
        return [10]


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

def nr_consoane(word):
  c = 0
  for i in word:
    if i not in "aeiouAEIOU":
      c += 1
  return c

def is_dale_chall(word):
  return int(word.lower() in DALE_CHALL)

def is_title(word):
  return int(word.istitle())

def nr_syllables(word):
  language = pyphen.Pyphen(lang='en')
  x = language.inserted(word).split('-')
  return len(x)

def morfologie(word):
    try:
        morf = wordnet.synsets(word)[0].pos()
        if morf == 'n':
            return 1
        elif morf == 'a':
            return 3
        elif morf == 'r':
            return 4
        else:
            return 2
    except Exception as e:
        return 0

def frecventa(word):
    return word_frequency(word, 'en')

def get_word_structure_features(word):
    features = []
    features.append(frecventa(word))
    features.append(is_dale_chall(word))
    features.append(len(word))
    features.append(nr_vowels(word))
    features.append(morfologie(word))
    return np.array(features)

def is_word_difficult(word,row):
    if word in textstat.difficult_words_list(row):
        return [1]
    return [0]

def synsets(word):
  return len(wordnet.synsets(word))

def hypernym_hypnoym(word):
    sum = 0
    for syn in wordnet.synsets(word):
            sum += len(syn.hypernyms())
    return sum

def get_wordnet_features(word):
  features = []
  features.append(hypernym_hypnoym(word))
  return np.array(features)

def get_readibilty_of_sentence(profile_text):
    return[textstat.dale_chall_readability_score_v2(profile_text)]


def featurize(row, vect):
    word = row['token']
    all_features = []
    all_features.extend(get_idf_score(vect, word))
    all_features.extend(corpus_feature(row['corpus']))
    all_features.extend(get_word_structure_features(word))
    all_features.extend(get_wordnet_features(word))
    all_features.extend(get_readibilty_of_sentence(row['sentence']))
    all_features.extend(is_word_difficult(word, row['sentence']))
    return np.array(all_features)

def featurize_df(df, vect):
    features = []
    for index, row in df.iterrows():
        row_ftrs = featurize(row, vect)
        features.append(row_ftrs)
    features = preprocessing.normalize(features)
    return features

results = train['complex']

X_train_compr, X_test_compr, y_train_compr, y_test_compr = train_test_split(train, results,
                                                                            test_size=0.20, stratify=results)

X_train_compr = X_train_compr.reset_index(drop=True)
X_test_compr = X_test_compr.reset_index(drop=True)
y_train_compr = y_train_compr.reset_index(drop=True)
y_test_compr = y_test_compr.reset_index(drop=True)

vectorizer, vect_train = get_idf_train(X_train_compr['sentence'])
vect_test = get_idf_test(vectorizer, X_test_compr['sentence'])

X_train = featurize_df(X_train_compr, vect_train)
X_test = featurize_df(X_test_compr, vect_test)

model1 = GaussianNB()
model1.fit(X_train, y_train_compr)
preds = model1.predict(X_test)

score1 = balanced_accuracy_score(y_test_compr, preds)
print(score1)
print('=======')

kfold = KFold(n_splits=10, shuffle=True)

array_score = []
array_matrix = []
cnt = 0

current = time.time()

for train_kfold, test_kfold in kfold.split(train):

    cnt += 1

    vectorizer, vect_train = get_idf_train(train.iloc[train_kfold]['sentence'])
    vect_test = get_idf_test(vectorizer, train.iloc[test_kfold]['sentence'])

    X_train = featurize_df(train.iloc[train_kfold], vect_train)
    X_test = featurize_df(train.iloc[test_kfold], vect_test)

    model = GaussianNB()
    model.fit(X_train, train.iloc[train_kfold]['complex'].values)
    preds = model.predict(X_test)

    score = balanced_accuracy_score(train.iloc[test_kfold]['complex'].values, preds)
    matrix = confusion_matrix(train.iloc[test_kfold]['complex'].values, preds)

    print("Numarul: " + str(cnt) + " " + str(score))

    array_score.append(score)
    array_matrix.append(matrix)

print("SECUNDE: " + str(time.time() - current))

print(np.mean(array_score))
print(sum(array_matrix))



vect_test = get_idf_test(vectorizer, test['sentence'])
X_test = featurize_df(test, vect_test)
preds = model.predict(X_test)
# #
df = pd.DataFrame()
df['id'] = test.index + len(train) + 1
df['complex'] = preds
df.to_csv('submission.csv', index=False)


