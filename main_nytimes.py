#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from data_source.twitter import TwitterObservable
from data_source.observer import Observer

import langid

from semantics import semantics_analysis
from trends import trends_analysis

from data_source import Logger

LOGGER = Logger.get_logger('Main-NYT')
NEG_COUNTER = 0
POS_COUNTER = 0

def detect_language(text):
    return langid.classify(text)


class NewArticleObserver(Observer):
    def update(self, update):
        lang = detect_language(update)

        # print str(lang)
        if lang[0] == 'en':
            print "Text:", update
            semantics = semantics_analysis.classify_text(update)
            print "Semantics:", semantics

            global NEG_COUNTER
            global POS_COUNTER
            if semantics == 'neg':
                NEG_COUNTER += 1
            else:
                POS_COUNTER += 1

            trends = trends_analysis.simple_top_words(
                # trends_analysis.get_golden_freq_dict(),
                trends_analysis.get_freq_dict_for_text(update)
            )
            print "Trends:", trends[:50]
            print("==============================================================================================")


map_TimeSemantics = {}
def calculate_semantics_changes(time, articles):
    neg_count = 0
    pos_count = 0

    from textblob import TextBlob
    for article in articles:
        blob = TextBlob(article['title'])

        if blob.sentiment.polarity > 0:
            pos_count += 1
        elif blob.sentiment.polarity < 0:
            neg_count += 1

    if time.year in map_TimeSemantics:
        map_TimeSemantics[time.year]['pos'] += pos_count
        map_TimeSemantics[time.year]['neg'] += neg_count
    else:
        map_TimeSemantics[time.year] = {
            'pos': pos_count,
            'neg': neg_count
        }


if __name__ == "__main__":
    observable = TwitterObservable()
    try:
        semantics_analysis.init()

        article_observer = NewArticleObserver()

        import datetime
        time = datetime.datetime(2000, 1, 1)
        end_time = datetime.datetime(2015, 11, 28)

        from data_source import nytimes
        while time < end_time:
            articles = nytimes.get_articles_for_day(time)

            calculate_semantics_changes(time, articles)

            # subtitles = ' '.join([(x['title'] if x['title'] is not None else '') for x in articles])
            # article_observer.update(subtitles)

            for article in articles:
                article_observer.update(article['title'] if article['title'] is not None else '')

            time = time + datetime.timedelta(days=1)

        # observable.register(article_observer)
        # observable.start_stream()
    except KeyboardInterrupt:
        observable.stop_stream()

        print 'Number of negative mentions', NEG_COUNTER
        print 'Number of positive mentions', POS_COUNTER
        pass
