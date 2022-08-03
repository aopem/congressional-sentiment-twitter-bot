from .politician import Politician
from .politician_type import PoliticianType

class Representative(Politician):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getType(self):
        return PoliticianType.Representative

    def getPossibleTwitterHandles(self):
        prefix = "Rep"
        possible = [f"{prefix}{self.first_name}{self.last_name}"]
        possible.append(f"{prefix}{self.last_name}")

        return possible
