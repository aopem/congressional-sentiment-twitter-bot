import json
import logging
from random import randrange

import django
from django.conf import settings

from sentiment_tweet_job.brokers import AzureKeyVaultBroker, AzureTextAnalyticsBroker, TwitterBroker
from sentiment_tweet_job.services import TextAnalyticsService, TwitterService
from sentiment_tweet_job.models import CongressMember
from sentiment_tweet_job.utils.constants import ENVIRONMENT, \
    TWITTER_MAX_TWEETS_RETURNED, AZURE_MAX_DOCUMENTS_PER_SENTIMENT_REQUEST

# setup django so ORM can be used without full framework
def django_init():
    if settings.configured:
        return

    # access Azure KeyVault for secrets
    appsettings_file_path = f"./appsettings.{ENVIRONMENT}.json"
    appsettings = json.loads(appsettings_file_path)
    keyvault_broker = AzureKeyVaultBroker(
        key_vault_name=appsettings["Azure"]["KeyVault"]["Name"]
    )

    # get db connection string secrets
    db_user = keyvault_broker.get_secret("CongressMemberDbUsername").value
    db_password = keyvault_broker.get_secret("CongressMemberDbPassword").value
    db_name = appsettings["Azure"]["Databases"]["CongressMember"]["DatabaseName"]
    db_host = appsettings["Azure"]["Databases"]["CongressMember"]["ServerName"]

    # configure db connection
    settings.configure(
        INSTALLED_APPS=[
            'sentiment_tweet_job',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'mssql',
                'NAME': db_name,
                'USER': db_user,
                'PASSWORD': db_password,
                'HOST': db_host,
                'PORT': '',
                'OPTIONS': {
                    'driver': 'ODBC Driver 18 for SQL Server'
                }
            }
        }
    )

    django.setup()


def main():
    # create brokers
    bot = TwitterBroker()
    text_analytics_broker = AzureTextAnalyticsBroker()

    # get all congress member IDs from db
    member_ids = CongressMember.objects.values_list(
        'id',
        flat=True
    )

    # select a random ID, then retrieve that member object
    # along with the corresponding twitter user
    rand_id = randrange(0, len(member_ids))
    member = CongressMember.objects.filter(
        id=rand_id
    )
    user = bot.get_user_by_name(
        username=member.twitter_account_name
    )

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
    if ENVIRONMENT == "Production":
        bot.tweet(
            text=sentiment_tweet
        )
    else:
        logging.info(f"Running in environment: {ENVIRONMENT}, will not send tweet unless in 'Production'")

    return


if __name__ == "__main__":
    django_init()
    main()
