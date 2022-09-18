from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential

import src.utils.functions as f

class AILanguageClient():
    """
    Client for interacting with Azure Cognitive Services

    Attributes:
        __credential (DefaultAzureCredential): credential to use
        for accessing Azure
        __client (TextAnalyticsClient): internal client for interacting
        with AI cognitive services
    """
    def __init__(
        self,
        endpoint: str
    ):
        """
        Constructor for AILanguageClient

        Args:
            endpoint (str): Azure cognitive services endpoint
        """
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
        """
        Gets sentiment for "text" sent to cognitive services endpoint

        Args:
            text (list[str]): list of strings to get sentiment for
            language (str, optional): language of text. Defaults to "en".
            show_opinion_mining (bool, optional): set to True to get more granular
            opinion analysis returned. Property "mined_opinions" will be present in
            analyzed_text if True. Defaults to True.

        Returns:
            list: list of analyzed sentiments
        """
        analyzed_text = self.__client.analyze_sentiment(
            documents=text,
            language=language,
            show_opinion_mining=show_opinion_mining
        )

        # filter out any errors and return
        return [text for text in analyzed_text if not text.is_error]
