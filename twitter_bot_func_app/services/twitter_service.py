from twitter_bot_func_app.model import TwitterAccount, SentimentScore
from twitter_bot_func_app.utils.constants import TWITTER_MAX_TWEETS_RETURNED

class TwitterService:
    """
    Service for performing Twitter operations
    """
    def create_sentiment_tweet(
        self,
        user: TwitterAccount,
        sentiment_score: SentimentScore
    ) -> str:
        text = f"Based on the {TWITTER_MAX_TWEETS_RETURNED} most recent mentions " \
               f"of #uscongress member @{user.username}, I have given them "       \
               f"a {sentiment_score.category} Twitter sentiment score of "         \
               f"{sentiment_score.value:.3f} (-1 to +1). I found "                 \
               f"{sentiment_score.num_positive} positive tweet(s) and "            \
               f"{sentiment_score.num_negative} negative tweet(s)"

        return text
