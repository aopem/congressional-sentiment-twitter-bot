"""
StrEnum defining allowed politician types
"""
from strenum import StrEnum

class PoliticianType(StrEnum):
    """
    Defines enumeration for Representative, Senator politician types
    """
    REPRESENTATIVE = 'REPRESENTATIVE'
    SENATOR = 'SENATOR'
