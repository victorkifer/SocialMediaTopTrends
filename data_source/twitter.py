__author__ = 'viktor'

from requests.packages.urllib3.exceptions import ProtocolError
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from observable import Observable


class _TweetsStreamListener(StreamListener):
    def __init__(self, api=None):
        super(_TweetsStreamListener, self).__init__(api)
        self.observer = None

    def set_observer(self, observer):
        self.observer = observer

    def on_status(self, status):
        if self.observer is not None:
            self.observer.update_observers(status.text)

    def on_error(self, status_code):
        print(str(status_code))


class TwitterObservable(Observable):
    def __init__(self):
        super(TwitterObservable, self).__init__()
        customer_key = "Twitter customer key"
        customer_secret = "Twitter customer secret"
        access_token = "Twitter access token"
        access_secret = "Twitter access secret"

        self.auth = OAuthHandler(customer_key, customer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.twitter_stream = None
        self.listener = _TweetsStreamListener()
        self.listener.set_observer(self)

    def start_stream(self):
        import requests
        requests.packages.urllib3.disable_warnings()

        try:
            self.twitter_stream = Stream(self.auth, self.listener)
            self.twitter_stream.filter(locations=[-180, -90, 180, 90])
        except ProtocolError:
            pass

    def stop_stream(self):
        if self.twitter_stream is not None:
            self.twitter_stream.disconnect()
            self.twitter_stream = None
