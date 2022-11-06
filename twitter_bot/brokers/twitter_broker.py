"""
Twitter API Broker
"""
import json
import tweepy

from .azure_keyvault_broker import AzureKeyVaultBroker
from twitter_bot.model import TwitterUser
from twitter_bot.utils.constants import SECRETS_FILEPATH, LOCAL_EXECUTION, TWITTER_TWEET_CHAR_LIMIT

class TwitterBroker():
    """
    Broker class for interacting with Twitter API

    Attributes:
        _tweepy_client (tweepy.Client): client for interacting with Twitter
    """
    def __init__(
        self,
        wait_on_rate_limit: bool = True
    ):
        """
        Constructor for Twitter Broker

        Args:
            wait_on_rate_limit (bool, optional): Set to false if this API
            broker should not synchronously wait when Twitter rate limits
            the API calls. Defaults to True.
        """
        self.__azure_keyvault_broker = AzureKeyVaultBroker()
        self.__api_secrets = self.__get_api_secrets_dict()
        self._tweepy_client = tweepy.Client(
            consumer_key=self.__api_secrets["apiKey"],
            consumer_secret=self.__api_secrets["apiKeySecret"],
            access_token=self.__api_secrets["accessToken"],
            access_token_secret=self.__api_secrets["accessTokenSecret"],
            bearer_token=self.__api_secrets["bearerToken"],
            wait_on_rate_limit=wait_on_rate_limit
        )

    def tweet(
        self,
        text: str
    ) -> dict:
        """
        Method for posting a tweet of "text" to Twitter

        Args:
            text (str): text that tweet will contain

        Returns:
            dict: response JSON dict from Twitter API
        """
        response = None

        # process tweet in chunks if too large
        if len(text) > TWITTER_TWEET_CHAR_LIMIT:
            chunks = self.__create_text_chunks(
                text=text
            )

            for chunk in chunks:
                response = self._tweepy_client.create_tweet(
                    text=chunk
                )
        else:
            response = self._tweepy_client.create_tweet(
                text=text
            )

        return response.data

    def search_username(
        self,
        username: str
    ) -> dict:
        """
        Searches for user @username on Twitter

        Args:
            username (str): username to search Twitter for

        Returns:
            dict: response JSON dict from Twitter API
        """
        response = self._tweepy_client.get_user(
            username=username,
            user_fields=["verified"]
        )

        return response.data

    def get_user_tweets(
        self,
        user: TwitterUser,
        max_results: int
    ) -> dict:
        """
        Returns up to max_results tweets from user

        Args:
            user (TwitterUser): user to obtain tweets from
            max_results (int): max number of tweets to return

        Returns:
            dict: response JSON dict from Twitter API, containing tweets
        """
        response = self._tweepy_client.get_users_tweets(
            id=user.id,
            max_results=max_results
        )

        return response.data

    def get_user_mentions(
        self,
        user: TwitterUser,
        max_results: int
    ) -> dict:
        """
        Get tweets mentioning user

        Args:
            user (TwitterUser): user being mentioned
            max_results (int): max number of tweets to return

        Returns:
            dict: response JSON dict from Twitter API, containing tweets
        """
        response = self._tweepy_client.get_users_mentions(
            id=user.id,
            max_results=max_results,
            tweet_fields=["lang"]
        )

        if response.data is None:
            return None

        return response.data

    def follow_user(
        self,
        user: TwitterUser
    ) -> dict:
        """
        Method for bot account to follow user

        Args:
            user (TwitterUser): user to follow

        Returns:
            dict: response JSON dict from Twitter API
        """
        response = self._tweepy_client.follow_user(user.id)
        return response.data

    def get_my_following(
        self
    ) -> dict:
        """
        Returns users bot account is following

        Returns:
            dict: response JSON dict from Twitter API
        """
        me = self._tweepy_client.get_me()
        response = self._tweepy_client.get_users_following(
            id=me.data.id,
            max_results=1000
        )

        return response.data

    def __create_text_chunks(
        self,
        text: str
    ) -> list[str]:
        """
        Splits text into chunks that each follow the format and
        character limit for an acceptable tweet

        Args:
            text (str): text to split into multiple tweets

        Returns:
            list[str]: list of properly formatted tweets
        """
        i = 0
        chunks = []
        while i + TWITTER_TWEET_CHAR_LIMIT < len(text):
            curr_chunk = text[i:i + TWITTER_TWEET_CHAR_LIMIT]
            chunks.append(curr_chunk)

            # increment for next chunk
            i += TWITTER_TWEET_CHAR_LIMIT

        # to get end bit of text
        chunks.append(text[i:])

        return chunks

    def __get_api_secrets_dict(self) -> dict:
        """
        Obtains a dictionary of all the required secrets. Uses secrets.json if running locally,
        otherwise uses the configured Azure Key Vault

        Returns:
            dict: dictionary object containing all needed secrets for twitter API access
        """
        if LOCAL_EXECUTION:
            return json.load(open(SECRETS_FILEPATH))

        api_secrets = [
            "apiKey",
            "apiKeySecret",
            "bearerToken",
            "clientId",
            "clientSecret",
            "accessToken",
            "accessTokenSecret"
        ]

        # get secrets from keyvault and build dict
        secrets_dict = {}
        for secret_name in api_secrets:
            secret = self.__azure_keyvault_broker.get_secret(
                name=secret_name
            )
            secrets_dict[secret_name] = secret.value

        return secrets_dict
