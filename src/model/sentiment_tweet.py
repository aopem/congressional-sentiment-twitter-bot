"""
Class representing a tweet about user sentiment
"""
from collections import defaultdict
from azure.ai.textanalytics import AnalyzeSentimentResult

from src.model.twitter_user import TwitterUser
from src.enums.sentiment import Sentiment

class SentimentTweet():
    """
    Represents a final tweet that details twitter sentiment about a user

    Attributes:
        __user (TwitterUser): twitter user being analyzed for sentiment
        sentiment_tracking_dict (dict): tracks all 4 sentiemnt types as defined
        in Sentiment() StrEnum
    """
    def __init__(
        self,
        user_analyzed: TwitterUser,
        sentiments: list[AnalyzeSentimentResult]
    ):
        """
        Constructor for SentimentTweet

        Args:
            user_analyzed (TwitterUser): user whose sentiment is being analyzed
            sentiments (list[AnalyzeSentimentResult]): list of sentiments obtained from
            AILanguageClient.getTextSentiment()
        """
        self.__user = user_analyzed

        # create dictionary from sentiments
        self.sentiment_tracking_dict = defaultdict(float)
        for item in sentiments:
            self.sentiment_tracking_dict[item.sentiment] += 1.0

    def getText(self) -> str:
        """
        Returns desired, formatted text containing tweet sentiment

        Returns:
            str: final tweet text (may be over character limit)
        """
        sentiment_score = self.__calculateSentimentScore()

        if sentiment_score > 0:
            score_category = "good"
        elif sentiment_score < 0:
            score_category = "poor"

        text = f"Based on the 100 most recent mentions of @{self.__user.username}, I have " \
               f"concluded that Twitter sentiment towards them is {score_category} " \
               f"with a score of {sentiment_score:.3f} (scale -1 to +1). "

        text += "I found:\n"
        text += f"{int(self.sentiment_tracking_dict[Sentiment.POSITIVE])} positive tweet(s)\n"
        text += f"{int(self.sentiment_tracking_dict[Sentiment.NEGATIVE])} negative tweet(s)\n\n"

        # hashtags
        text += "#congress"

        return text

    def __calculateSentimentScore(self) -> float:
        """
        Calculates a sentiment score based on all sentiments given, which
        will be between -1.0 and +1.0. A positive number indicates positive
        sentiment and a negative number indicates negative sentiment.

        Returns:
            float: sentiment score between -1.0 and +1.0
        """
        sentiment_score = 1.0 * self.sentiment_tracking_dict[Sentiment.POSITIVE]
        sentiment_score += -1.0 * self.sentiment_tracking_dict[Sentiment.NEGATIVE]

        # do not want to include 'mixed' sentiment tweets as valid
        num_valid_sentiments = self.sentiment_tracking_dict[Sentiment.POSITIVE] + \
            self.sentiment_tracking_dict[Sentiment.NEGATIVE] + \
            self.sentiment_tracking_dict[Sentiment.NEUTRAL]

        return sentiment_score / num_valid_sentiments
