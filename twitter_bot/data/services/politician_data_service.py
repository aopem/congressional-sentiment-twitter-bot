"""
Service for interacting with politician data
"""
import re
import logging

from twitter_bot.data import Politician, WikipediaDataBroker
from twitter_bot.brokers import TwitterBroker
from twitter_bot.model import TwitterUser
from twitter_bot.enums import PoliticianType
from twitter_bot.utils.constants import TWITTER_USERNAME_CHARACTER_LIMIT, \
    TWITTER_USERNAME_REGEX_PATTERN

class PoliticianDataService:
    """
    Service for interacting with politician data
    """
    def __init__(
        self,
        rep_wiki_data_broker: WikipediaDataBroker,
        sen_wiki_data_broker: WikipediaDataBroker,
        twitter_broker: TwitterBroker
    ):
        self.__rep_data_broker = rep_wiki_data_broker
        self.__sen_data_broker = sen_wiki_data_broker
        self.__twitter_broker = twitter_broker

    def get_politician_list(
        self,
        politician_type: PoliticianType
    ) -> list[Politician]:
        """
        Gets a list of Politician objects

        Args:
            politician_type (PoliticianType): type of politician list to obtain

        Raises:
            Exception: Raised if invalid politician_type passed

        Returns:
            list[Politician]: list of Politician objects
        """
        if politician_type == PoliticianType.REPRESENTATIVE:
            keys = {
                "name_key": "Member",
                "party_key": "Party.1",
                "state_key": "District",
                "residence_key": "Residence",
                "date_born_key": "Born[2]"
            }

            data = self.__rep_data_broker.get_table()
        elif politician_type == PoliticianType.SENATOR:
            keys = {
                "name_key": "Senator",
                "party_key": "Party.1",
                "state_key": "State",
                "residence_key": "Residence[2]",
                "date_born_key": "Born"
            }

            data = self.__sen_data_broker.get_table()
        else:
            error = f"Invalid politician type: {politician_type}"
            logging.error(error)
            raise Exception(error)

        # process data and add to a list
        politician_list = []
        for politician in data.values():
            try:
                name = politician[keys["name_key"]].split()

                politician_list.append(Politician(
                    first_name=name[0],
                    last_name=name[1] if len(name) <= 2 else name[2],
                    party=politician[keys["party_key"]],
                    state=politician[keys["state_key"]],
                    residence=politician[keys["residence_key"]],
                    date_born=politician[keys["date_born_key"]],
                    politician_type=politician_type
                ))

            except IndexError:
                logging.warn(f"Name {politician[name_key]} not formatted correctly")

        return politician_list

    def create_politician_list(
        self,
        data: dict
    ) -> list[Politician]:
        """
        Create a list[Politician] from JSON data

        Args:
            data (dict): serialized JSON list of Politician objects

        Returns:
            list[Politician]: list of Politician objects
        """
        politician_list = []
        for politician in data:
            if politician["type"] != PoliticianType.REPRESENTATIVE or \
               politician["type"] != PoliticianType.SENATOR:
                logging.error(f"Invalid politician type {politician['type']}")
                continue

            politician_list.append(Politician(
                first_name=politician["first_name"],
                last_name=politician["last_name"],
                party=politician["party"],
                state=politician["state"],
                residence=politician["residence"],
                date_born=politician["date_born"],
                politician_type=type
            ))

        return politician_list

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

    def search_possible_twitter_usernames(
        self,
        possible_usernames: list[str]
    ) -> TwitterUser:
        for username in possible_usernames:
            possible_user = self.__twitter_broker.search_username(
                username=username
            )

            # if user is found, possible_user will be populated
            if possible_user is None:
                continue

            # if user retrieved is not verified, then continue
            if not possible_user.verified:
                continue

            # if above checks pass, will return as a real account
            return TwitterUser(
                id=possible_user.id,
                name=possible_user.name,
                username=possible_user.username,
                verified=possible_user.verified
            )

        return None

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
