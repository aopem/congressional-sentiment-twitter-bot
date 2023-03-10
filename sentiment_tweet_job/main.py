import json
import logging
logging.basicConfig(level=logging.INFO)

from random import randrange, uniform

from sentiment_tweet_job.brokers import AzureTextAnalyticsBroker, \
    AzureKeyVaultBroker, TwitterBroker, CongressMemberApiBroker
from sentiment_tweet_job.services import TextAnalyticsService, TwitterService
from sentiment_tweet_job.models import TwitterAccount, SentimentAnalysis
from sentiment_tweet_job.utils.constants import ENVIRONMENT, \
    TWITTER_MAX_TWEETS_RETURNED, AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST


def main():
    # get configuration
    appsettings = json.load(open(f"./appsettings.{ENVIRONMENT}.json"))

    # create and inject dependencies
    azure_keyvault_broker = AzureKeyVaultBroker(configuration=appsettings)
    text_analytics_broker = AzureTextAnalyticsBroker(configuration=appsettings)
    congress_member_api_broker = CongressMemberApiBroker(configuration=appsettings)
    bot = TwitterBroker(azure_keyvault_broker=azure_keyvault_broker)

    # get all congress member IDs from db
    members = congress_member_api_broker.get_all()

    # select a random ID, then retrieve that member object
    # along with the corresponding twitter user
    rand_index = randrange(0, len(members))
    member = members[rand_index]

    while member["twitterAccountName"] is None:
        message = f"Congress member {member['firstName']} {member['lastName']} does not have a Twitter account. " \
            f"Finding a new account to analyze..."
        logging.info(message)

        # randomly select another member
        rand_index = randrange(0, len(members))
        member = members[rand_index]

    logging.info(f"Successfully randomly selected {member['firstName']} {member['lastName']} (@{member['twitterAccountName']}, ID: {member['id']})")
    user = bot.get_user_by_name(
        username=member["twitterAccountName"]
    )

    user_account = TwitterAccount(
        id=user["id"],
        name=user["name"],
        username=user["username"],
        verified=user["verified"]
    )

    # get tweets up to TWITTER_MAX_TWEETS_RETURNED to analyze
    logging.info(f"Using Twitter user ID: {user_account.id}")
    mentions = bot.get_user_mentions(
        user=user_account,
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
    twitter_service = TwitterService()
    text_analytics_service = TextAnalyticsService()
    sentiments = []

    # only perform actual sentiment analysis in Production
    logging.info("Obtaining tweet sentiment...")
    if ENVIRONMENT == "Production":
        for i in range(0, stop, step):
            batch = text_analytics_broker.get_text_sentiment(
                text=mention_list[i:i + step]
            )

            # add all elements of batch to sentiment list
            for analysis in batch:
                sentiments.append(analysis)

        sentiment_analysis = text_analytics_service.get_sentiment_analysis(
            sentiments=sentiments
        )
    else:
        # simulate a sentiment analysis
        sentiment_analysis = SentimentAnalysis(
            score=uniform(-1.0, 1.0),
            num_positive=randrange(0, 33),
            num_negative=randrange(0, 33),
            num_neutral=randrange(0, 33),
            num_mixed=0
        )

    sentiment_tweet = twitter_service.create_sentiment_tweet(
        user=user,
        sentiment_analysis=sentiment_analysis
    )
    logging.info(f"Full tweet text ({len(sentiment_tweet)} characters):")
    logging.info(f"{sentiment_tweet}")

    # send tweet to Twitter
    if ENVIRONMENT == "Production":
        bot.tweet(
            text=sentiment_tweet
        )
    else:
        logging.info(f"Running in environment: '{ENVIRONMENT}', will not send tweet unless in 'Production'")

    return


if __name__ == "__main__":
    main()
