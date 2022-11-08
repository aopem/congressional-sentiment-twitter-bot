from twitter_bot_func_app.data import Politician
from .twitter_account import TwitterAccount

class PoliticianTwitterAccount(TwitterAccount):
    def __init__(
        self,
        politician: Politician,
        **kwargs
    ):
        self.politician = politician
        super().__init__(**kwargs)
