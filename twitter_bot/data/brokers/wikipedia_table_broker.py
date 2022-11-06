"""
Class for interacting with tables on a Wikipedia page
"""
import logging
import pandas as pd

class WikipediaTableBroker:
    def __init__(
        self,
        wiki_url: str,
        size: int
    ):
        self.__wiki_url = wiki_url
        self.__size = size

    def get_table(self) -> dict:
        """
        Returns a dict representation of the table requested

        Raises:
            Exception: Returned if no table of the proper size found

        Returns:
            dict: Dictionary representation of the requested table
        """
        wiki_data = pd.read_html(self.__wiki_url)

        # find correct table according to list_size
        for df in wiki_data:
            size = df.shape[0]
            if size == self.__size:
                return df.to_dict(orient='index')

        error = f"No table of size {self.__size} found at URL: {self.__wiki_url}"
        logging.error(error)
        raise Exception(error)
