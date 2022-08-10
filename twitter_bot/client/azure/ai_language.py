from typing import Text
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

import twitter_bot.utils.functions as f


class AILanguageClient():
    def __init__(
        self,
        endpoint: str
    ):
        self.__credential = DefaultAzureCredential(
            managed_identity_client_id=f.get_msi_client_id()
        )
        self.__client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=self.__credential
        )

    def getTextSentiment(
        self,
        text: list
    )