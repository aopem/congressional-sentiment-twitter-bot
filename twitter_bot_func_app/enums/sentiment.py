"""
StrEnum defining different sentiment types
"""
from strenum import StrEnum

class Sentiment(StrEnum):
    """
    Maps sentiment keys from Azure to enum values
    """
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    NEGATIVE = 'negative'
    MIXED = 'mixed'
