import re
import constants as c

class Politician:
    def __init__(self, first_name, last_name, party, state, residence, date_born):
        self.first_name = first_name
        self.last_name = last_name
        self.party = party
        self.state = state
        self.residence = residence
        self.date_born = date_born

    def getPoliticianType(self):
        raise NotImplementedError()

    def getPossibleTwitterHandles(self):
        raise NotImplementedError()

    def _filterTwitterHandles(self, unfiltered_possible_handles):
        possible_handles = []
        for possible_handle in unfiltered_possible_handles:
            valid_handle = self.__getValidTwitterHandle(possible_handle)
            if valid_handle:
                possible_handles.append(valid_handle)

        return possible_handles

    def _verifyUser(self):
        pass

    def __getValidTwitterHandle(self, possible_handle):
        if len(possible_handle) > c.TWITTER_USERNAME_CHARACTER_LIMIT:
            possible_handle = possible_handle[:c.TWITTER_USERNAME_CHARACTER_LIMIT]

        if not re.match(c.TWITTER_USERNAME_REGEX_PATTERN, possible_handle):
            return None

        return possible_handle


