from .politician import Politician
from .politician_type import PoliticianType

class Senator(Politician):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getPoliticianType(self):
        return PoliticianType.Senator

    def getPossibleTwitterHandles(self):
        prefixes = []
        prefixes.append("Sen")
        prefixes.append("Senator")

        unfiltered_possible_handles = []
        for prefix in prefixes:
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}")

        return super()._filterTwitterHandles(unfiltered_possible_handles)