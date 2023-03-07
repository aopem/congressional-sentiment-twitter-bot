import requests
import logging

class CongressMemberApiBroker:
    def __init__(
        self,
        configuration: dict
    ):
        port = configuration["CongressMemberApi"]["Port"]
        host = configuration["CongressMemberApi"]["Host"]
        self.__endpoint = f"http://{host}:{port}/api/"

    def get_all(
        self
    ) -> list[dict]:
        """
        Retrieves all Congress members from database using
        REST API endpoint

        Returns:
            list[dict]: all Congress Members in database
        """
        request_url = f"{self.__endpoint}CongressMember"
        response = requests.get(
            url=request_url
        )

        return response.json()
