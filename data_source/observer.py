__author__ = 'viktor'

from abc import ABCMeta, abstractmethod


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, update):
        pass
