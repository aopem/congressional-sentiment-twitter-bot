import json
import azure.functions as func
import logging

from twitter_bot.client.twitter import BotClient
from twitter_bot.model import TwitterUser
import twitter_bot.utils.constants as c
import twitter_bot.utils.functions as f


def run(
    in_found: str
):
    # create bot client
    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    # create set of users already following
    logging.info("Retrieving currently followed users from Twitter...")
    following = bot.getFollowing()
    following_ids = {}
    for user in following:
        following_ids.add(user.id)

    # read json containing twitter account info
    logging.info("Loading twitter accounts to follow from getusers/found.json...")
    twitter_user_json = json.loads(in_found)

    # follow all users - no errors if already following
    for user_json in twitter_user_json:
        if user_json["id"] not in following_ids:
            user = TwitterUser(
                id=user_json["id"],
                name=user_json["name"],
                username=user_json["username"],
                verified=user_json["verified"]
            )

            try:
                bot.followUser(user)
                logging.info(f"Successfully followed @{user.username} ({user.name})")
            except Exception:
                logging.warn(f"Could not follow user @{user.username} ({user.name})")

    return


def main(
    inFound: str,
):
    run(inFound)


if __name__ == "__main__":
    main()
