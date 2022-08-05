from twitter_bot.enums import PoliticianType
from .politician import Politician

class Representative(Politician):
    def getPoliticianType(self):
        return PoliticianType.REPRESENTATIVE

    def getPossibleTwitterHandles(self):
        prefixes = []
        prefixes.append("Rep")
        prefixes.append("Congressman")
        prefixes.append("Congresswoman")
        prefixes.append("Congressmember")

        unfiltered_possible_handles = []
        unfiltered_possible_handles.append(f"{self.first_name}{self.last_name}")
        for prefix in prefixes:
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}")

        return super()._filterTwitterHandles(unfiltered_possible_handles)
