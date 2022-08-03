from .politician import Politician
from .politician_type import PoliticianType

class Representative(Politician):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getPoliticianType(self):
        return PoliticianType.Representative

