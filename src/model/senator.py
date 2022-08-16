"""
Senator class
"""
from src.enums import PoliticianType
from .politician import Politician

class Senator(Politician):
    """
    Class defining a Senator

    Attributes:
        name (str): Senator name
        party (str): affiliated party
        state (str): state representing
        residence (str): where Senator is located
        date_born (str): when Senator was born
        type (PoliticianType): type as defined by PoliticianType enum
    """
    def __init__(
        self,
        kwargs
    ):
        super().__init__(**kwargs)
        self.type = PoliticianType.SENATOR

    def getPossibleTwitterHandles(self) -> list[str]:
        """
        Returns a list of possible Twitter handles/usernames for this Senator

        Returns:
            list[str]: list of possible Twitter usernames for this Senator
        """
        prefixes = []
        prefixes.append("Sen")
        prefixes.append("Senator")

        unfiltered_possible_handles = []
        unfiltered_possible_handles.append(f"{self.first_name}{self.last_name}")
        for prefix in prefixes:
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.last_name}")
            unfiltered_possible_handles.append(f"{prefix}{self.first_name}")

        return super()._filterTwitterHandles(
            unfiltered_possible_handles=unfiltered_possible_handles
        )
