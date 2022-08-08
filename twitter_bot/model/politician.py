import re
from twitter_bot.utils import constants as c

class Politician:
    def __init__(
        self,
        name,
        party,
        state,
        residence,
        date_born
    ):
        name_list = name.split()
        self.first_name = name_list[0]
        self.last_name = name_list[1] if len(name_list) <= 2 else name_list[2]
        self.name = name
        self.party = party
        self.state = state
        self.residence = residence
        self.date_born = date_born

    def getPossibleTwitterHandles(self):
        raise NotImplementedError()

    def _filterTwitterHandles(
        self,
        unfiltered_possible_handles
    ):
        possible_handles = []
        for possible_handle in unfiltered_possible_handles:
            valid_handle = self.__getValidTwitterHandle(possible_handle)
            if valid_handle:
                possible_handles.append(valid_handle)

        return possible_handles

    def __getValidTwitterHandle(
        self,
        possible_handle
    ):
        if len(possible_handle) > c.TWITTER_USERNAME_CHARACTER_LIMIT:
            possible_handle = possible_handle[:c.TWITTER_USERNAME_CHARACTER_LIMIT]

        if not re.match(c.TWITTER_USERNAME_REGEX_PATTERN, possible_handle):
            return None

        return possible_handle
