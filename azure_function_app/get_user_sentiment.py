import json
import argparse

import twitter_bot.utils.constants as c
from twitter_bot.client import BotClient
from twitter_bot.model import TwitterUser


def run(index):
    bot = BotClient(c.SECRETS_FILEPATH)

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--index',
        type=int,
        required=True
    )

    args = parser.parse_args()

    run(args.index)


if __name__ == "__main__":
    main()
