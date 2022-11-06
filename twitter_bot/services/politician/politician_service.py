"""
Service for working with Politician objects
"""

from twitter_bot.model import Politician

class PoliticianService:
    def __init__(self):
        pass

    def add_politician(
        self,
        politician: Politician
    ):
        return