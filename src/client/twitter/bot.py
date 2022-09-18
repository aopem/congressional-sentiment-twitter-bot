import tweepy
from src.model import TwitterUser
import src.utils.constants as c

class BotClient:
    """
    Client class for interacting with Twitter bot

    Attributes:
        __client (tweept.Client): class for interacting
        with Twitter API
    """
    def __init__(
        self,
        api_key: str,
        api_key_secret: str,
        access_token: str,
        access_token_secret: str,
        bearer_token: str,
        wait_on_rate_limit: bool = True
    ):
        """
        Constructor for BotClient

        Args:
            api_key (str): Twitter web app API key
            api_key_secret (str): Twitter web app API key secret
            access_token (str): Twitter web app access token
            access_token_secret (str): Twitter web app access token secret
            bearer_token (str): Twitter web app bearer token
            wait_on_rate_limit (bool, optional): Dictates whether client will
            synchronously block and wait when rate-limited. Defaults to True.
        """
        # create tweepy client
        self.__client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
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
        if len(text) > c.TWITTER_TWEET_CHAR_LIMIT:
            chunks = self.__createTextChunks(
                text=text
            )

            for chunk in chunks:
                response = self.__client.create_tweet(
                    text=chunk
                )
        else:
            response = self.__client.create_tweet(
                text=text
            )

        return response.data

    def searchUsername(
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
        response = self.__client.get_user(
            username=username,
            user_fields=["verified"]
        )

        return response.data

    def getUserTweets(
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
        response = self.__client.get_users_tweets(
            id=user.id,
            max_results=max_results
        )

        return response.data

    def getUserMentions(
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
        response = self.__client.get_users_mentions(
            id=user.id,
            max_results=max_results,
            tweet_fields=["lang"]
        )

        if response.data is None:
            return None

        return response.data

    def followUser(
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
        response = self.__client.follow_user(user.id)
        return response.data

    def getMyFollowing(
        self
    ) -> dict:
        """
        Returns users bot account is following

        Returns:
            dict: response JSON dict from Twitter API
        """
        me = self.__client.get_me()
        response = self.__client.get_users_following(
            id=me.data.id,
            max_results=1000
        )

        return response.data

    def __createTextChunks(
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
        while i + c.TWITTER_TWEET_CHAR_LIMIT < len(text):
            curr_chunk = text[i:i + c.TWITTER_TWEET_CHAR_LIMIT]
            chunks.append(curr_chunk)

            # increment for next chunk
            i += c.TWITTER_TWEET_CHAR_LIMIT

        # to get end bit of text
        chunks.append(text[i:])

        return chunks
