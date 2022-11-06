"""
Politician base class
"""
import re
from twitter_bot.utils.constants import TWITTER_USERNAME_CHARACTER_LIMIT, TWITTER_USERNAME_REGEX_PATTERN

class Politician:
    """
    Base class defining a general Politician

    Attributes:
        first_name (str): first name
        last_name (str): last name
        name (str): Politician full name
        party (str): affiliated party
        state (str): state representing
        residence (str): where Politician is located
        date_born (str): when Politician was born
    """
    def __init__(
        self,
        first_name: str,
        last_name: str,
        party: str,
        state: str,
        residence: str,
        date_born: str
    ):
        # name_list = name.split()
        # self.first_name = name_list[0]
        # self.last_name = name_list[1] if len(name_list) <= 2 else name_list[2]
        self.first_name = first_name
        self.last_name = last_name
        self.name = f"{first_name} {last_name}"
        self.party = party
        self.state = state
        self.residence = residence
        self.date_born = date_born

    def getPossibleTwitterHandles(self):
        """
        A method that should return a list of possible Twitter handles/usernames
        for this particular politician

        Raises:
            NotImplementedError: Raised if not implemented by child class
        """
        raise NotImplementedError()

    def _filterTwitterHandles(
        self,
        unfiltered_possible_handles: list[str]
    ) -> list[str]:
        """
        Filters out any Twitter handles that don't meet the guidelines for a
        Twitter username

        Args:
            unfiltered_possible_handles (list[str]): unfiltered list of possible Twitter handles
            for this politician

        Returns:
            list[str]: filtered list of politician handles that does not contain any usernames
            that are invalid according to Twitter standards
        """
        possible_handles = []
        for possible_handle in unfiltered_possible_handles:
            valid_handle = self.__getValidTwitterHandle(
                possible_handle=possible_handle
            )
            if valid_handle:
                possible_handles.append(valid_handle)

        return possible_handles

    def __getValidTwitterHandle(
        self,
        possible_handle: str
    ) -> str:
        """
        Checks if possible_handle can be a legitimate Twitter username

        Args:
            possible_handle (str): possible Twitter username

        Returns:
            str: a valid Twitter handle, else returns None
        """
        if len(possible_handle) > TWITTER_USERNAME_CHARACTER_LIMIT:
            possible_handle = possible_handle[:TWITTER_USERNAME_CHARACTER_LIMIT]

        if not re.match(TWITTER_USERNAME_REGEX_PATTERN, possible_handle):
            return None

        return possible_handle
