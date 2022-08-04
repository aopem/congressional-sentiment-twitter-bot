from .politician import Politician
from .politician_type import PoliticianType

class Representative(Politician):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getPoliticianType(self):
        return PoliticianType.Representative

    def getPossibleTwitterHandles(self):
        prefix = "Rep"
        unfiltered_possible_handles = []
        unfiltered_possible_handles.append(f"{self.first_name}{self.last_name}")
        unfiltered_possible_handles.append(f"{prefix}{self.first_name}{self.last_name}")
        unfiltered_possible_handles.append(f"{prefix}{self.last_name}")
        unfiltered_possible_handles.append(f"{prefix}{self.first_name}")

        return super()._filterTwitterHandles(unfiltered_possible_handles)