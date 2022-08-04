import json
from .twitter_account import TwitterAccount
from .politician import Politician

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, TwitterAccount, Politician):
            return o.__dict__
        return super().default(o)
