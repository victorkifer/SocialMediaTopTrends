__author__ = 'victor'

from sklearn.externals import joblib
from logger import log

import collections
import nltk.classify.util, nltk.metrics

from nltk.metrics import scores
from nltk.classify import NaiveBayesClassifier
from nltk.classify.decisiontree import DecisionTreeClassifier

import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

from nltk.corpus import stopwords

_STOPSET = set(stopwords.words('english'))

_MODEL = None
_CLASSIFIER_ALGORITHM = NaiveBayesClassifier
_MODEL_FILE = ('Semantics_%s.mdl' % _CLASSIFIER_ALGORITHM.__name__)


def init():
    _load_model()
    if _MODEL is None:
        _create_model()
        _save_model()


def get_model():
    return _MODEL


def _load_model():
    log('Loading DTC model')
    try:
        global _MODEL
        _MODEL = joblib.load(_MODEL_FILE)
    except IOError, e:
        print 'Cannot load model', e
    pass


def _save_model():
    log('Saving model for future use')
    if _MODEL is not None:
        joblib.dump(_MODEL, _MODEL_FILE)
        log('Model is saved')
    pass


def _create_model():
    log('Creating model from input data')

    clf = _evaluate_classifier(_stopword_filtered_word_feats)

    global _MODEL
    _MODEL = clf

    log('Model is created')
    pass


def _word_feats(words):
    return dict([(word, True) for word in words])


def _stopword_filtered_word_feats(words):
    return dict([(word, True) for word in words if word not in _STOPSET])


def _bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=100):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])


def _evaluate_classifier(featx):
    from nltk.corpus import movie_reviews

    print "Loading file ids"
    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    print "Loading features"
    negfeats = [(featx(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(featx(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats) * 3 / 4
    poscutoff = len(posfeats) * 3 / 4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

    print "Training"
    classifier = _CLASSIFIER_ALGORITHM.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', scores.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', scores.recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', scores.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', scores.recall(refsets['neg'], testsets['neg'])
    classifier.show_most_informative_features()
    return classifier


def classify_text(text):
    feats = _bigram_word_feats(_stopword_filtered_word_feats(_word_feats(text)))
    semantics = _MODEL.classify(feats)
    return semantics
