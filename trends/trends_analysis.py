# -*- coding: utf-8 -*-

__author__ = 'victor'

from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import brown

from nltk.corpus import stopwords

import re

import operator

_THRESHOLD = 0.4

_URL_REGEX = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''';

_tokenizer = RegexpTokenizer(r'\w+')

def get_freq_dict_for_text(text):
    # remove urls
    text = text.lower()
    text = re.sub(_URL_REGEX, '', text, flags=re.MULTILINE)

    words = _tokenizer.tokenize(text)
    words = [word.lower() for word in words]
    freq_dict = FreqDist(words)
    return freq_dict


def get_golden_freq_dict():
    words = brown.words()
    words = [word.lower() for word in words]
    freq_dict = FreqDist(words)
    return freq_dict


def compute_top_trends(golden_dict, freq_dict):
    words = set(freq_dict.keys())
    top_words = []

    stop_set = stopwords.words('english')

    total_golden_dict = sum(golden_dict.values())
    total_freq_dict = sum(freq_dict.values())

    for word in words:
        if word in stop_set:
            continue
        if re.match(r"^[^\w]$", word):
            continue

        golden_freq = golden_dict[word] if word in golden_dict else 0
        current_freq = freq_dict[word] if word in freq_dict else 0

        rel_golden_freq = golden_freq * 1.0 / total_golden_dict
        rel_current_freq = current_freq * 1.0 / total_freq_dict

        item = (word, abs(rel_golden_freq - rel_current_freq))
        top_words.append(item)

    top_words.sort(key=operator.itemgetter(1), reverse=True)

    return top_words


def simple_top_words(freq_dict):
    words = set(freq_dict.keys())
    top_words = []

    stop_set = stopwords.words('english')

    for word in words:
        if word in stop_set:
            continue
        if re.match(r"^[^\w]$", word):
            continue

        current_freq = freq_dict[word] if word in freq_dict else 0

        item = (word, current_freq)
        top_words.append(item)

    top_words.sort(key=operator.itemgetter(1), reverse=True)

    return top_words
