"""
Sentiment Score class
"""
from twitter_bot_func_app.enums import SentimentScoreCategory

class SentimentAnalysis:
    """
    Score calculated based on a list of given sentiments. Value should be
    between -1.0 and +1.0, where negative/positive indicate negative or positive
    general sentiment

    Attributes:
        value (float): value of sentiment score
        num_positive (int): num positive sentiments
        num_negative (int): num negative sentiments
        num_neutral (int): num neutral sentiments
        num_mixed (int): num mixed sentiments
        category (SentimentScoreCategory): enum dictating score classification
    """
    def __init__(
        self,
        score: float,
        num_positive: int,
        num_negative: int,
        num_neutral: int,
        num_mixed: int,
        category: SentimentScoreCategory = SentimentScoreCategory.NEUTRAL
    ):
        self.score = score
        self.num_positive = num_positive
        self.num_negative = num_negative
        self.num_neutral = num_neutral
        self.num_mixed = num_mixed
        self.category = category
