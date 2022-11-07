"""
StrEnum defining different sentiment score categories
"""
from strenum import StrEnum

class SentimentScoreCategory(StrEnum):
    """
    Maps sentiment score to a category
    """
    GOOD = 'GOOD'
    POOR = 'POOR'
    NEUTRAL = 'NEUTRAL'
