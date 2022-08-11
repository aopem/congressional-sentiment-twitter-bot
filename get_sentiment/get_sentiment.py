import json
from collections import defaultdict
import logging
import azure.functions as func

from src.client.twitter import BotClient
from src.client.azure import AILanguageClient
from src.model import TwitterUser
import src.utils.functions as f
import src.utils.constants as c


def run(
    current_index: int,
    in_found: str
) -> int:
    # get secrets and create clients
    secrets = f.get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))
    language = AILanguageClient(
        endpoint=azure_config["resourceGroup"]["cognitiveServices"]["account"]["endpoint"]
    )

    # read json containing twitter account info
    user_json = f.load_json(in_found)
    if user_json is None:
        logging.error("Could not load getusers/found.json, exiting...")
        return (current_index + 1) % len(user_json)

    # get element at current_index
    user_json = user_json[current_index]
    user = TwitterUser(
        id=user_json["id"],
        name=user_json["name"],
        username=user_json["username"],
        verified=user_json["verified"]
    )
    logging.info(f"inFound[{current_index}]: {user_json}")

    # get tweets up to TWITTER_MAX_TWEETS_RETURNED to analyze
    mentions = bot.getUserMentions(
        user=user,
        max_results=c.TWITTER_MAX_TWEETS_RETURNED
    )

    # return if no mentions found
    if mentions is None:
        logging.warn(f"No mentions for @{user.username} ({user.name}) found, exiting...")
        return

    # create single list of all mention text, output in logs
    mention_list = [mention.text for mention in mentions]
    for i, mention in enumerate(mention_list):
        logging.info(f"mention_list[{i}] = {mention}")

    # calculate variables for range()
    # need to send requests in batches of 10 (max request size)
    stop = len(mention_list)
    step = c.AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST

    # get sentiment of tweets, assuming all in English
    logging.info("Obtaining tweet sentiment...")
    sentiment = []
    for i in range(0, stop, step):
        batch = language.getTextSentiment(
            text=mention_list[i:i + step]
        )

        # add all elements of batch to sentiment list
        for analysis in batch:
            sentiment.append(analysis)

    sentiment_tracking_dict = defaultdict(list)
    for item in sentiment:
        confidence_score = item.confidence_scores.get(item.sentiment)
        if confidence_score is None:
            confidence_score = 0

        sentiment_tracking_dict[item.sentiment].append(confidence_score)
        logging.info(f"Sentiment: {item.sentiment}, Confidence: {confidence_score}")

    # now, create and post a tweet containing the found info
    tweet = f"@{user.username} based on your recent mentions, " \
            f"here is the sentiment about you on Twitter:\n" \

    # append sentiment values from dict to tweet
    for sentiment, confidence_score_list in sentiment_tracking_dict.items():
        tweet += f"{len(confidence_score_list)} {sentiment} tweet(s), confidence = "

        avg_confidence_score = sum(confidence_score_list)/float(len(confidence_score_list))
        avg_confidence_score = f"{avg_confidence_score:.2f}"
        if sentiment == "mixed":
            avg_confidence_score = "N/A"

        tweet += f"{avg_confidence_score}\n"

    logging.info(f"Full tweet text ({len(tweet)} characters):")
    logging.info(f"{tweet}")

    # send tweet to Twitter
    bot.tweet(
        text=tweet
    )

    # mod by len(user_json) so index will wrap around at last item
    return (current_index + 1) % len(user_json)


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
    next_index = run(
        current_index=current_index,
        in_found=inFound
    )

    outCurrentIndex.set(str(next_index))
    logging.info(f"[OUT] getusersentiment/current_index: {outCurrentIndex.get()}")


if __name__ == "__main__":
    main()
