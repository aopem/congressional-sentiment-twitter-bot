import tweepy
import json

class TweepyClient:
    def __init__(self, secrets_file_name):
        secrets_json = json.load(open(secrets_file_name))

        # create tweepy client using secrets
        self.__client = tweepy.Client(
            consumer_key=secrets_json["API_KEY"],
            consumer_secret=secrets_json["API_KEY_SECRET"],
            access_token=secrets_json["ACCESS_TOKEN"],
            access_token_secret=secrets_json["ACCESS_TOKEN_SECRET"],
            bearer_token=secrets_json["BEARER_TOKEN"],
            wait_on_rate_limit=True
        )

    def searchUsername(self, username):
        response = self.__client.get_user(username=username, user_fields=["verified"])
        return response

    def getUserTweets(self, user, max_results):
        response = self.__client.get_users_tweets(id=user.id, max_results=max_results)
        return response