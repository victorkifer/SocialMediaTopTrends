__author__ = 'victor'

from datetime import datetime


def log(message):
    current_time = datetime.now().time().isoformat()
    print current_time, message
