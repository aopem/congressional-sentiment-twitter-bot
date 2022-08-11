import tweepy
from src.model import TwitterUser
import src.utils.constants as c

class BotClient:
    def __init__(
        self,
        api_key: str,
        api_key_secret: str,
        access_token: str,
        access_token_secret: str,
        bearer_token: str,
        wait_on_rate_limit: bool = True
    ):
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
        response = self.__client.get_users_tweets(
            id=user.id,
            max_results=max_results
        )

        return response.data

    def getTweetReplies(
        self,
        tweet,
        max_results
    ):
        pass
        # TODO: currently broken, fix this function
        # response = self.__client.get_tweet(
        #     id=tweet.id,
        #     tweet_fields=["conversation_id"]
        # )

        # print(response.data)
        # conversation_id = 0
        # for response_tweet in response:
        #     print(f"response_tweet: {response_tweet}")
        #     if response_tweet.data["conversation_id"]:
        #         print(f"conversation_id: {response_tweet.data['conversation_id']}")
        #         conversation_id = response_tweet.data["conversation_id"]
        #         break

        # conversation_tweets = self.__client.search_recent_tweets(
        #     query=f"conversation_id:{conversation_id}",
        #     max_results=max_results,
        #     expansions=["referenced_tweets.id", "in_reply_to_user_id"]
        # )

        # return conversation_tweets

    def getUserMentions(
        self,
        user: TwitterUser,
        max_results: int
    ) -> dict:
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
        response = self.__client.follow_user(user.id)
        return response.data

    def getMyFollowing(
        self
    ) -> dict:
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
