"""
Politician base class
"""
from twitter_bot.enums import PoliticianType

class Politician:
    """
    Base class defining a general Politician

    Attributes:
        first_name (str): first name
        last_name (str): last name
        party (str): affiliated party
        state (str): state representing
        residence (str): where Politician is located
        date_born (str): when Politician was born
        politician_type (PoliticianType): type of Politician
    """
    def __init__(
        self,
        first_name: str,
        last_name: str,
        party: str,
        state: str,
        residence: str,
        date_born: str,
        politician_type: PoliticianType
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.party = party
        self.state = state
        self.residence = residence
        self.date_born = date_born
        self.politician_type = politician_type
