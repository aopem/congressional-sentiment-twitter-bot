from typing import List, Text
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
        text: list[str],
        *,
        language: str = "en",
        show_opinion_mining: bool = True,
    ) -> list:
        analyzed_text = self.__client.analyze_sentiment(
            documents=text,
            language=language,
            show_opinion_mining=show_opinion_mining
        )

        # filter out any errors and return
        return [text for text in analyzed_text if not text.is_error]
