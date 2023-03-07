from sentiment_tweet_job.models import TwitterAccount, SentimentAnalysis
from sentiment_tweet_job.utils.constants import TWITTER_MAX_TWEETS_RETURNED

class TwitterService:
    """
    Service for performing Twitter operations
    """
    def create_sentiment_tweet(
        self,
        user: TwitterAccount,
        sentiment_analysis: SentimentAnalysis
    ) -> str:
        text = f"Based on the {TWITTER_MAX_TWEETS_RETURNED} most recent mentions " \
               f"of #uscongress member @{user.username}, I have given them "       \
               f"a {sentiment_analysis.category} Twitter sentiment score of "      \
               f"{sentiment_analysis.value:.3f} (-1 to +1). I found "              \
               f"{sentiment_analysis.num_positive} positive tweet(s) and "         \
               f"{sentiment_analysis.num_negative} negative tweet(s)"

        return text
