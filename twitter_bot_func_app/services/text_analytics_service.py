from collections import defaultdict
from azure.ai.textanalytics import AnalyzeSentimentResult

from twitter_bot_func_app.model import SentimentScore
from twitter_bot_func_app.enums import Sentiment, SentimentScoreCategory

class TextAnalyticsService:
    """
    Service for performing text analytics
    """
    def get_sentiment_score(
        self,
        sentiments: list[AnalyzeSentimentResult]
    ) -> SentimentScore:
        """
        Calculates a sentiment score based on all sentiments given, which
        will be between -1.0 and +1.0. A positive number indicates positive
        sentiment and a negative number indicates negative sentiment.

        Returns:
            SentimentScore: sentiment score between -1.0 and +1.0
        """
        # create dictionary from sentiments
        sentiment_dict = defaultdict(float)
        for item in sentiments:
            sentiment_dict[item.sentiment] += 1.0

        raw_score = sentiment_dict[Sentiment.POSITIVE] - sentiment_dict[Sentiment.NEGATIVE]

        # do not want to include 'mixed' sentiment tweets as valid
        num_valid_sentiments = sentiment_dict[Sentiment.POSITIVE] + \
            sentiment_dict[Sentiment.NEGATIVE] + \
            sentiment_dict[Sentiment.NEUTRAL]

        sentiment_score = SentimentScore(
            value=raw_score / num_valid_sentiments,
            num_positive=sentiment_dict[Sentiment.POSITIVE],
            num_negative=sentiment_dict[Sentiment.NEGATIVE],
            num_neutral=sentiment_dict[Sentiment.NEUTRAL],
            num_mixed=sentiment_dict[Sentiment.MIXED],
        )

        if sentiment_score.value > 0:
            sentiment_score.category = SentimentScoreCategory.GOOD

        if sentiment_score.value < 0:
            sentiment_score.category = SentimentScoreCategory.POOR

        return sentiment_score
