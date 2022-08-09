import json
from twitter_bot.model import TwitterUser
from twitter_bot.model.politician import Politician

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (TwitterUser, Politician)):
            return o.__dict__
        return super().default(o)
