"""
Custom JSON encoder class
"""
import json
from twitter_bot_func_app.model import TwitterAccount
from twitter_bot_func_app.model.politician import Politician

class Encoder(json.JSONEncoder):
    """
    Custom JSON encoder to make user-defined python classes serializable to JSON
    """
    def default(
        self,
        o: any
    ) -> any:
        """
        Default encoder behavior. Will use the '__dict__' attribute of an instance
        of TwitterAccount or Politician for JSON encoding, otherwise uses default
        JSON encoder behavior

        Args:
            o (Any): An object that will be serialized to JSON

        Returns:
            Any: Serialized JSON object
        """
        if isinstance(o, (TwitterAccount, Politician)):
            return o.__dict__
        return super().default(o)
