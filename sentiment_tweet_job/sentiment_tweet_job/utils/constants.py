"""
All constant values are stored here
"""
import os

# twitter limits
TWITTER_USERNAME_CHARACTER_LIMIT = 15
TWITTER_USERNAME_REGEX_PATTERN = r"^[A-Za-z0-9_]{1,15}$"
TWITTER_MAX_RESULTS_RETURNED = 10
TWITTER_MAX_TWEETS_RETURNED = 100
TWITTER_TWEET_CHAR_LIMIT = 280

# azure limits
AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST = 10

# see if running in development or production environment
ENVIRONMENT = os.environ["ENVIRONMENT"] if os.environ["ENVIRONMENT"] is not None else "Development"
