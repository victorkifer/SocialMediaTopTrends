__author__ = 'victor'

import datetime
import urllib2

import Logger

LOGGER = Logger.get_logger('NYTimes')

_API_KEY = "Put your NY Time API key here"

_API_URL = "http://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date=%s&end_date=%s&api-key=" + _API_KEY

_CACHE_DIR = "nytimes_articles"

import os, errno
import os.path
import shutil

def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_cache_file(file):
    _mkdir_p(_CACHE_DIR)

    old_file_path = _CACHE_DIR + "/articles_" + file + ".json"

    new_file_dir = _CACHE_DIR + "/" + file[:4] + "/" + file[4:6]
    _mkdir_p(new_file_dir)
    new_file_path = new_file_dir + "/articles_" + file[6:] + ".json"

    if not os.path.isfile(new_file_path):
        if os.path.isfile(old_file_path):
            shutil.move(old_file_path, new_file_path)

    return new_file_path


def get_from_cache(date_str):
    filename = get_cache_file(date_str)

    if not os.path.isfile(filename):
        return None

    with file(filename) as f:
        return f.read()


def save_to_cache(date_str, page):
    filename = get_cache_file(date_str)

    with file(filename, 'w+') as f:
        f.write(page)


def __fetch_file(link):
    LOGGER.debug("Fetching %s", link)

    req = urllib2.Request(link)  # , data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


def get_articles_for_day(time):
    date_str = time.isoformat(' ').split()[0].replace("-", "")
    # date_str = time.strftime("%Y%m%d")
    LOGGER.debug("Loading articles for date %s", date_str)

    page = get_from_cache(date_str)
    if page is not None:
        LOGGER.debug("Loaded from cache")
    else:
        request_url = _API_URL % (date_str, date_str)
        page = __fetch_file(request_url)
        save_to_cache(date_str, page)

    return parse_article(page)


def parse_article(page):
    import json
    obj = json.loads(page)

    if obj['status'] != 'OK':
        return []

    articles = []
    for doc in obj['response']['docs']:
        if 'main' not in doc['headline']:
            continue

        article = {
            'title': doc['headline']['main'],
            'subtitle': doc['lead_paragraph'],
            'snippet': doc['snippet'],
            'category': doc['section_name'],
            'date': doc['pub_date']
        }

        articles.append(article)

    return articles

