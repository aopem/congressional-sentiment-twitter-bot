"""
Azure Cloud broker class
"""
import os
import json
import logging
import requests
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AccessToken

from twitter_bot.utils.constants import AZURE_CONFIG_FILEPATH, SECRETS_FILEPATH, LOCAL_EXECUTION

class AzureCloudBroker():
    """
    Broker for interacting with Azure cloud

    Attributes:
        __config (dict): JSON dict of cloud configuration
        __subscription_id (str): subscription ID to work with
        __resource_group (str): resource group to work with
        __msi_name (str): name of MSI to authenticate as
        __api_version (str): API version used with MSI
        __msi_client_id (str): client ID of MSI for authentication
    """
    def __init__(self):
        self._config = json.load(
            open(AZURE_CONFIG_FILEPATH)
        )
        self._subscription_id = self._config["subscriptionId"]
        self._resource_group = self._config["resourceGroup"]["name"]
        self.__msi_name = self._config["resourceGroup"]["managedIdentity"]["name"]
        self.__api_version = self._config["resourceGroup"]["managedIdentity"]["restApiVersion"]
        self.__msi_client_id = self.__get_msi_client_id()

    def authenticate(self) -> AccessToken:
        """
        Authenticates to Azure and returns an access token

        Returns:
            AccessToken: credential to authenticate to Azure
        """
        return DefaultAzureCredential(
            managed_identity_client_id=self.__msi_client_id
        )

    def __get_msi_client_id(
        self
    ) -> str:
        """
        Gets the MSI client ID for the specified managed identity from the MSI REST endpoint

        REST endpoint reference:
        https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp#rest-endpoint-reference

        Raises:
            Exception: Indicates the MSI client ID could not be obtained

        Returns:
            str: MSI client ID string
        """
        # if running locally, get MSI from secrets.json
        if LOCAL_EXECUTION:
            return json.load(open(SECRETS_FILEPATH))["msiClientId"]

        endpoint = os.getenv("IDENTITY_ENDPOINT")
        headers = {"X-IDENTITY-HEADER": os.getenv("IDENTITY_HEADER")}

        # build MSI resource ID for API query
        msi_resource_id = f"/subscriptions/{self.__subscription_id}/resourcegroups" \
                          f"/{self.__resource_group}/providers" \
                          f"/Microsoft.ManagedIdentity/userAssignedIdentities/{self.__msi_name}"

        # build auth URI for REST API query
        auth_uri = f"{endpoint}?resource=https://vault.azure.net&api-version={self.__api_version}" \
                   f"&mi_res_id={msi_resource_id}"

        response = requests.get(url=auth_uri, headers=headers)
        if response.status_code == 500:
            exception = f"Status code = 500, could not retrieve MSI client ID from endpoint\n" \
                        f"Request URI: {auth_uri}"
            logging.error(exception)
            raise Exception(exception)

        return response.json()["client_id"]
