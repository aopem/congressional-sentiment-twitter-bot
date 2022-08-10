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
    user = user_json[current_index]
    logging.info(f"inFound[{current_index}]: {user}")

    # get tweets up to TWITTER_MAX_TWEETS_RETURNED to analyze
    mentions = bot.getUserMentions(
        user=TwitterUser(
            id=user["id"],
            name=user["name"],
            username=user["name"],
            verified=user["verified"]
        ),
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
    outCurrentIndex: func.Out[str],
    context: func.Context
):
    logging.info(f"Executing function: {context.function_name}")
    logging.info(f"Invocation ID: {context.invocation_id}")
    logging.info(f"[IN] getusersentiment/current_index: {inCurrentIndex}")

    current_index = 0
    try:
        current_index = int(inCurrentIndex)
    except Exception as e:
        logging.warn(f"Caught exception {e}, current_index set to 0")

    # run function, then increment index by 1 and output
    run(
        current_index=current_index,
        in_found=inFound
    )

    outCurrentIndex.set(current_index + 1)
    logging.info(f"[OUT] getusersentiment/current_index: {outCurrentIndex.get()}")


if __name__ == "__main__":
    main()
