from .politician import Politician
from .politician_type import PoliticianType

class Senator(Politician):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getType(self):
        return PoliticianType.Senator

    def getPossibleTwitterHandles(self):
        prefix = "Sen"
        possible = [f"{prefix}{self.first_name}{self.last_name}"]
        possible.append(f"{prefix}{self.last_name}")

        prefix = "Senator"
        possible.append(f"{prefix}{self.first_name}{self.last_name}")
        possible.append(f"{prefix}{self.last_name}")

        return possible