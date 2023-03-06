"""
Azure Function for analyzing sentiment of a Twitter user
"""
import logging
import azure.functions as func

from twitter_bot_app.brokers import TwitterBroker, AzureTextAnalyticsBroker
from twitter_bot_app.services import TwitterService, TextAnalyticsService
from twitter_bot_app.model import TwitterAccount, SentimentTweet
from twitter_bot_app.utils.functions import load_json
from twitter_bot_app.utils.constants import AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST, \
    TWITTER_MAX_TWEETS_RETURNED


def run(
    current_index: int,
    in_found: str
) -> int:
    # create Azure, Twitter brokers
    bot = TwitterBroker()
    text_analytics_broker = AzureTextAnalyticsBroker()

    # read json containing twitter account info
    user_list = load_json(in_found)
    if user_list is None:
        logging.error("Could not load getusers/found.json, exiting...")
        return (current_index + 1) % len(user_list)

    # get element at current_index
    user_json = user_list[current_index]
    user = TwitterAccount(
        id=user_json["id"],
        name=user_json["name"],
        username=user_json["username"],
        verified=user_json["verified"]
    )
    logging.info(f"inFound[{current_index}]: {user_json}")

    # get tweets up to TWITTER_MAX_TWEETS_RETURNED to analyze
    mentions = bot.get_user_mentions(
        user=user,
        max_results=TWITTER_MAX_TWEETS_RETURNED
    )

    # return if no mentions found
    if mentions is None:
        logging.warning(f"No mentions for @{user.username} ({user.name}) found, exiting...")
        return

    # create single list of all mention text, output in logs
    mention_list = [mention.text for mention in mentions]
    for i, mention in enumerate(mention_list):
        logging.info(f"mention_list[{i}] = {mention}")

    # calculate variables for range()
    # need to send requests in batches of 10 (max request size)
    stop = len(mention_list)
    step = AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST

    # get sentiment of tweets, assuming all in English
    logging.info("Obtaining tweet sentiment...")
    sentiments = []
    for i in range(0, stop, step):
        batch = text_analytics_broker.get_text_sentiment(
            text=mention_list[i:i + step]
        )

        # add all elements of batch to sentiment list
        for analysis in batch:
            sentiments.append(analysis)

    text_analytics_service = TextAnalyticsService()
    twitter_service = TwitterService()
    sentiment_analysis = text_analytics_service.get_sentiment_analysis(
        sentiments=sentiments
    )
    sentiment_tweet = twitter_service.create_sentiment_tweet(
        user=user,
        sentiment_analysis=sentiment_analysis
    )

    logging.info(f"Full tweet text ({len(sentiment_tweet)} characters):")
    logging.info(f"{sentiment_tweet}")

    # send tweet to Twitter
    bot.tweet(
        text=sentiment_tweet
    )

    # mod by len(user_json) so index will wrap around at last item
    return (current_index + 1) % len(user_list)


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
    except Exception as ex:
        logging.warning(f"Caught exception {ex}, current_index set to 0")

    # run function, then increment index by 1 and output
    next_index = run(
        current_index=current_index,
        in_found=inFound
    )

    outCurrentIndex.set(str(next_index))
    logging.info(f"[OUT] getusersentiment/current_index: {outCurrentIndex.get()}")


if __name__ == "__main__":
    main()
