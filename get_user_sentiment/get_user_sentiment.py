import json
import argparse
import azure.functions as func

import twitter_bot.utils.constants as c
from twitter_bot.client.twitter import BotClient
from twitter_bot.model import TwitterUser
import twitter_bot.utils.functions as f


def run(index):
    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    # read json containing twitter account info
    user_json = json.load(open(c.TWITTER_ACCOUNTS_FOUND_FILENAME))[index]
    user = TwitterUser(
        id=user_json["id"],
        name=user_json["name"],
        username=user_json["name"],
        verified=user_json["verified"]
    )

    # get tweets up to TWITTER_MAX_TWEETS_RETURNED to analyze
    mentions = bot.getUserMentions(
        user=user,
        max_results=c.TWITTER_MAX_TWEETS_RETURNED
    )

    # return if no mentions found
    if mentions is None:
        print(f"WARN: No mentions for @{user.username} ({user.name}) found, exiting...")
        return

    # get sentiment of tweets
    # TODO: use azure text analytics
    for mention in mentions:
        # TODO: analyze sentiment of mention.text
        pass

    return


def main(timer: func.TimerRequest):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--index',
        type=int,
        required=True
    )

    args = parser.parse_args()

    if timer.past_due:
        run(args.index)


if __name__ == "__main__":
    main()
