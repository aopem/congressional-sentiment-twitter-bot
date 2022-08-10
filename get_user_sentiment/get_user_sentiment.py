import logging
import azure.functions as func

from twitter_bot.client.twitter import BotClient
from twitter_bot.model import TwitterUser
import twitter_bot.utils.functions as f
import twitter_bot.utils.constants as c


def run(
    current_index: int,
    in_found: str
):
    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    # read json containing twitter account info
    user_json = f.load_json(in_found)
    if user_json is None:
        logging.error("Could not load getusers/found.json, exiting...")
        return

    # get element at current_index
    user_json = user_json[current_index]
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
        logging.warn(f"No mentions for @{user.username} ({user.name}) found, exiting...")
        return

    # get sentiment of tweets
    # TODO: use azure text analytics
    for mention in mentions:
        # TODO: analyze sentiment of mention text
        pass

    return


def main(
    timer: func.TimerRequest,
    inFound: str,
    inCurrentIndex: str,
    outCurrentIndex: func.Out[str]
):
    current_index = int(inCurrentIndex)

    # run function, then increment index by 1 and output
    run(
        current_index=current_index,
        in_found=inFound
    )

    outCurrentIndex.set(current_index + 1)


if __name__ == "__main__":
    main()
