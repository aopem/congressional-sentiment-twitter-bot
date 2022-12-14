"""
Azure Function for analyzing sentiment of a Twitter user
"""
import json
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

from src.client.twitter import BotClient
from src.client.azure import AILanguageClient
from src.model import TwitterUser
from src.model import SentimentTweet
from src.utils.functions import get_secrets_dict, get_msi_client_id, load_json
from src.utils.constants import AZURE_CONFIG_FILEPATH, \
    AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST, TWITTER_MAX_TWEETS_RETURNED


def run(
    current_index: int,
    in_found: str
) -> int:
    # get secrets and create clients
    secrets = get_secrets_dict()
    bot = BotClient(
        api_key=secrets["apiKey"],
        api_key_secret=secrets["apiKeySecret"],
        access_token=secrets["accessToken"],
        access_token_secret=secrets["accessTokenSecret"],
        bearer_token=secrets["bearerToken"]
    )

    azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
    credential = DefaultAzureCredential(
        managed_identity_client_id=get_msi_client_id(
            subscription_id=azure_config["subscriptionId"],
            resource_group=azure_config["resourceGroup"]["name"],
            msi_name=azure_config["resourceGroup"]["managedIdentity"]["name"],
            api_version=azure_config["resourceGroup"]["managedIdentity"]["restApiVersion"]
        )
    )
    language = AILanguageClient(
        credential=credential,
        endpoint=azure_config["resourceGroup"]["cognitiveServices"]["account"]["endpoint"]
    )

    # read json containing twitter account info
    user_list = load_json(in_found)
    if user_list is None:
        logging.error("Could not load getusers/found.json, exiting...")
        return (current_index + 1) % len(user_list)

    # get element at current_index
    user_json = user_list[current_index]
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
        batch = language.getTextSentiment(
            text=mention_list[i:i + step]
        )

        # add all elements of batch to sentiment list
        for analysis in batch:
            sentiments.append(analysis)

    tweet = SentimentTweet(
        user_analyzed=user,
        sentiments=sentiments
    )

    logging.info(f"Full tweet text ({len(tweet.getText())} characters):")
    logging.info(f"{tweet.getText()}")

    # send tweet to Twitter
    bot.tweet(
        text=tweet.getText()
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
    except Exception as e:
        logging.warning(f"Caught exception {e}, current_index set to 0")

    # run function, then increment index by 1 and output
    next_index = run(
        current_index=current_index,
        in_found=inFound
    )

    outCurrentIndex.set(str(next_index))
    logging.info(f"[OUT] getusersentiment/current_index: {outCurrentIndex.get()}")


if __name__ == "__main__":
    main()
