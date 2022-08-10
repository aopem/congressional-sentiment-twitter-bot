import tweepy

class BotClient:
    def __init__(
        self,
        api_key,
        api_key_secret,
        access_token,
        access_token_secret,
        bearer_token,
        wait_on_rate_limit=True
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

    def searchUsername(
        self,
        username
    ):
        return self.__client.get_user(
            username=username,
            user_fields=["verified"]
        )

    def getUserTweets(
        self,
        user,
        max_results
    ):
        return self.__client.get_users_tweets(
            id=user.id,
            max_results=max_results
        )

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
        user,
        max_results
    ):
        response = self.__client.get_users_mentions(
            id=user.id,
            max_results=max_results
        )

        if response.data is None:
            return None

        return response.data

    def followUser(
        self,
        user
    ):
        return self.__client.follow_user(user.id)

    def getFollowing(
        self
    ):
        me = self.__client.get_me()
        response = self.__client.get_users_following(
            id=me.data.id,
            max_results=1000
        )

        return response.data