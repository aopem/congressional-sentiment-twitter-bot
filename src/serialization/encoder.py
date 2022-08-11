import json
from src.model import TwitterUser
from src.model.politician import Politician

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (TwitterUser, Politician)):
            return o.__dict__
        return super().default(o)
