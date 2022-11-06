"""
Service for getting a Twitter username of a Politician object
"""

from twitter_bot.utils.constants import TWITTER_USERNAME_CHARACTER_LIMIT, TWITTER_USERNAME_REGEX_PATTERN

class TwitterPoliticianUsernameService:
    def __init__(self):
        pass

    def get_possible_twitter_usernames(
        self,
        first_name: str,
        last_name: str
    ):
        """
        A method that should return a list of possible Twitter handles/usernames
        for this particular politician

        Raises:
            NotImplementedError: Raised if not implemented by child class
        """
        raise NotImplementedError()


    def _filter_twitter_usernames(
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
