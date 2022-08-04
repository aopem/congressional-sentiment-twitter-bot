import json
from .twitter_account import TwitterAccount
from .politician import Politician

class Encoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, TwitterAccount) or \
           isinstance(object, Politician):
            return object.__dict__
        else:
            return super().default(object)