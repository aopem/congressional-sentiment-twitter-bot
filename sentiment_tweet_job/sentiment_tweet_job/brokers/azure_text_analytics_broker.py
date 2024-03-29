"""
Azure Text Analytics Broker class
"""
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult
from azure.identity import DefaultAzureCredential

class AzureTextAnalyticsBroker():
    """
    Client for interacting with Azure Cognitive Services

    Attributes:
        __text_analytics_client (TextAnalyticsClient): internal client
        for interacting with AI cognitive services
    """
    def __init__(
        self,
        configuration: dict
    ):
        cognitive_services_account = configuration["Azure"]["CognitiveServices"]["AccountName"]
        self.__text_analytics_client = TextAnalyticsClient(
            endpoint=f"https://{cognitive_services_account}.cognitiveservices.azure.com/",
            credential=DefaultAzureCredential()
        )

    def get_text_sentiment(
        self,
        text: list[str],
        *,
        language: str = "en",
        show_opinion_mining: bool = True,
    ) -> list[AnalyzeSentimentResult]:
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
        analyzed_text = self.__text_analytics_client.analyze_sentiment(
            documents=text,
            language=language,
            show_opinion_mining=show_opinion_mining
        )

        # filter out any errors and return
        return [text for text in analyzed_text if not text.is_error]
