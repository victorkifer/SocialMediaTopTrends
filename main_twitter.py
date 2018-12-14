#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from data_source.twitter import TwitterObservable
from data_source.observer import Observer

import langid

from semantics import semantics_analysis
from trends import trends_analysis


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

            trends = trends_analysis.compute_top_trends(
                trends_analysis.get_golden_freq_dict(),
                trends_analysis.get_freq_dict_for_text(update)
            )
            print "Trends:", trends[:50]
            print("==============================================================================================")


if __name__ == "__main__":
    observable = TwitterObservable()

    try:
        semantics_analysis.init()

        article_observer = NewArticleObserver()
        observable.register(article_observer)

        observable.start_stream()
    except KeyboardInterrupt:
        observable.stop_stream()
        pass
