#!/usr/bin/python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

from datetime import datetime
import json
import codecs

from data_source.twitter import TwitterObservable
from data_source.observer import Observer


def totimestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def current_timestamp():
    now = datetime.utcnow()
    return totimestamp(now)


class NewArticleObserver(Observer):
    def update(self, update):
        update = update.replace('\n', ' ').replace('\r', ' ')

        time = current_timestamp()

        json_obj = json.dumps({'time': time, 'text': update})

        with codecs.open('/media/Data/twitter.txt', 'a', encoding='utf8') as myfile:
            myfile.write(json_obj)
            myfile.write(u"\n")


if __name__ == "__main__":
    try:
        observable = TwitterObservable()

        article_observer = NewArticleObserver()
        observable.register(article_observer)

        observable.start_stream()
    except KeyboardInterrupt:
        pass
