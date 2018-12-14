#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from data_source import Logger
import logging

Logger._LOG_LEVEL = logging.DEBUG

if __name__ == "__main__":
    import datetime
    time = datetime.datetime(1851, 9, 18)
    end_time = datetime.datetime(1900, 1, 1)

    from data_source import nytimes
    while time < end_time:
        articles = nytimes.get_articles_for_day(time)

        time = time + datetime.timedelta(days=1)
