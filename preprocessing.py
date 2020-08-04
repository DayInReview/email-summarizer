import re
import string
import joblib

import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

nltk.download('punkt')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

### Word Cleaning ###

def remove_stop_words(words):
    return [i for i in words if i not in ENGLISH_STOP_WORDS]


def word_stemmer(words):
    return [stemmer.stem(o) for o in words]


def word_lemmatizer(words):
    return [lemmatizer.lemmatize(o) for o in words]


def clean_word(text):
    text = word_tokenize(text)
    cleaning_utils = [remove_stop_words,
                      word_stemmer,
                      word_lemmatizer]
    for o in cleaning_utils:
        text = o(text)
    return text


### Sentence Cleaning ###

def remove_hyperlink(word):
    return re.sub(r"http\S+", "", word)


def to_lower(word):
    return word.lower()


def remove_number(word):
    return re.sub(r'\d+', '', word)


def remove_punctuation(word):
    return word.translate(str.maketrans(dict.fromkeys(string.punctuation)))


def remove_whitespace(word):
    return word.strip()


def replace_newline(word):
    return word.replace('\n','')


def clean_sentence(text):
    cleaning_utils = [remove_hyperlink,
                      replace_newline,
                      to_lower,
                      remove_number,
                      remove_punctuation,
                      remove_whitespace]
    for o in cleaning_utils:
        text = o(text)
    return text


### Tokenization ###

def tokenize(text):
    tokenizer = joblib.load('keras/models/tokenizer.tk')
    text_sequence = np.array(tokenizer.texts_to_sequences([text,]))
    text_sequence = pad_sequences(text_sequence, maxlen=2000)


def preprocess(text):
    text = clean_sentence(text)
    text = clean_word(text)
    return tokenize(text)
