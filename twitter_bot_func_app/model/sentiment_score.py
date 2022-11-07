from twitter_bot_func_app.enums import SentimentScoreCategory

class SentimentScore:
    def __init__(
        self,
        value: float,
        num_positive: int,
        num_negative: int,
        num_neutral: int,
        num_mixed: int,
        category: SentimentScoreCategory = SentimentScoreCategory.NEUTRAL
    ):
        self.value = value
        self.num_positive = num_positive
        self.num_negative = num_negative
        self.num_neutral = num_neutral
        self.num_mixed = num_mixed
        self.category = category
