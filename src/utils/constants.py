"""
All constant values are stored here
"""
from pathlib import Path
from os.path import exists

ROOT_DIR = Path(__file__).parent.parent.parent

# senator/representative constants
REPRESENTATIVES_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
SENATORS_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
TOTAL_NUM_REPRESENTATIVES = 435
TOTAL_NUM_SENATORS = 100

# twitter limits
TWITTER_USERNAME_CHARACTER_LIMIT = 15
TWITTER_USERNAME_REGEX_PATTERN = r"^[A-Za-z0-9_]{1,15}$"
TWITTER_MAX_RESULTS_RETURNED = 10
TWITTER_MAX_TWEETS_RETURNED = 100
TWITTER_TWEET_CHAR_LIMIT = 280

# azure limits
AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST = 10

# config files
SECRETS_FILEPATH = f"{ROOT_DIR}/secrets.json"
AZURE_CONFIG_FILEPATH = f"{ROOT_DIR}/config.azure.json"

# see if local execution - secrets only stored locally
LOCAL_EXECUTION = exists(SECRETS_FILEPATH)
