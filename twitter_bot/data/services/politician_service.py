"""
Service for a Politician object
"""
import re
import logging

from twitter_bot.data import Politician
from twitter_bot.enums import PoliticianType
from twitter_bot.utils.constants import TWITTER_USERNAME_CHARACTER_LIMIT, \
    TWITTER_USERNAME_REGEX_PATTERN

class PoliticianService:
    """
    Service for a Politician object
    """
    def __init__(self):
        pass

    def get_possible_twitter_usernames(
        self,
        politician: any
    ) -> list[str]:
        """
        A method that should return a list of possible Twitter handles/usernames
        for this particular politician

        Raises:
            Exception: Raised if incorrect object type passed
        """
        if politician.politician_type == PoliticianType.REPRESENTATIVE:
            prefixes = [
                "Rep",
                "Congressman",
                "Congresswoman",
                "Congressmember"
            ]
        elif politician.politician_type == PoliticianType.SENATOR:
            prefixes = [
                "Sen",
                "Senator"
            ]
        else:
            error = f"Object passed is of type {type(politician)}, " \
                    f"should be Representative or Senator"
            logging.error(error)
            raise Exception(error)

        return self.__get_twitter_usernames(
            politician=politician,
            prefixes=prefixes
        )

    def __get_twitter_usernames(
        self,
        politician: Politician,
        prefixes: list[str]
    ) -> list[str]:
        """
        Returns a list of possible Twitter handles/usernames for this Representative

        Args:
            politician (Politician): Politician object to get usernames for
            prefixes (list[str]): list of prefixes that should be used for username generation

        Returns:
            list[str]: list of possible Twitter usernames for this Representative
        """
        unfiltered_usernames = []
        unfiltered_usernames.append(f"{politician.first_name}{politician.last_name}")
        for prefix in prefixes:
            unfiltered_usernames.append(f"{prefix}{politician.first_name}{politician.last_name}")
            unfiltered_usernames.append(f"{prefix}{politician.last_name}")
            unfiltered_usernames.append(f"{prefix}{politician.first_name}")

        return self.__filter_twitter_usernames(
            unfiltered_usernames=unfiltered_usernames
        )

    def __filter_twitter_usernames(
        self,
        unfiltered_usernames: list[str]
    ) -> list[str]:
        """
        Filters out any Twitter handles that don't meet the guidelines for a
        Twitter username

        Args:
            unfiltered_usernames (list[str]): unfiltered list of possible Twitter handles
            for this politician

        Returns:
            list[str]: filtered list of politician handles that does not contain any usernames
            that are invalid according to Twitter standards
        """
        filtered_usernames = []
        for possible_username in unfiltered_usernames:
            valid_username = self.__get_valid_twitter_username(
                possible_username=possible_username
            )

            if valid_username:
                filtered_usernames.append(valid_username)

        return filtered_usernames

    def __get_valid_twitter_username(
        self,
        possible_username: str
    ) -> str:
        """
        Checks if possible_username can be a legitimate Twitter username

        Args:
            possible_username (str): possible Twitter username

        Returns:
            str: a valid Twitter handle, else returns None
        """
        if len(possible_username) > TWITTER_USERNAME_CHARACTER_LIMIT:
            possible_username = possible_username[:TWITTER_USERNAME_CHARACTER_LIMIT]

        if not re.match(TWITTER_USERNAME_REGEX_PATTERN, possible_username):
            return None

        return possible_username
