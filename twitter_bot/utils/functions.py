"""
Miscellaneous utility functions
"""
import os
import json
import logging
import requests
from azure.identity import DefaultAzureCredential

import twitter_bot.client.azure as azclient
from .constants import SECRETS_FILEPATH, AZURE_CONFIG_FILEPATH, LOCAL_EXECUTION


def get_secrets_dict() -> dict:
    """
    Obtains a dictionary of all the required secrets. Uses secrets.json if running locally,
    otherwise uses the configured Azure Key Vault

    Returns:
        dict: dictionary object containing all secrets listed in keyvault secrets from the
        Azure config file
    """
    if LOCAL_EXECUTION:
        return json.load(open(SECRETS_FILEPATH))

    azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
    credential = DefaultAzureCredential(
        managed_identity_client_id=get_msi_client_id(
            subscription_id=azure_config["subscriptionId"],
            resource_group=azure_config["resourceGroup"]["name"],
            msi_name=azure_config["resourceGroup"]["managedIdentity"]["name"],
            api_version=azure_config["resourceGroup"]["managedIdentity"]["restApiVersion"]
        )
    )
    keyvault = azclient.KeyVaultClient(
        credential=credential,
        key_vault_name=azure_config["resourceGroup"]["keyVault"]["name"],
    )

    # get secrets from keyvault and build dict
    secrets_dict = {}
    for secret_name in azure_config["resourceGroup"]["keyVault"]["secrets"]:
        secret = keyvault.getSecret(
            name=secret_name
        )
        secrets_dict[secret_name] = secret.value

    return secrets_dict


def get_msi_client_id(
    subscription_id: str,
    resource_group: str,
    msi_name: str,
    api_version: str
) -> str:
    """
    Gets the MSI client ID for the specified managed identity from the MSI REST endpoint

    REST endpoint reference:
    https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp#rest-endpoint-reference

    Args:
        subscription_id (str): subscription ID for MSI
        resource_group (str): name of resource group for MSI
        msi_name (str): name of MSI
        api_version (str): MSI REST API endpoint version to use

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
    msi_resource_id = f"/subscriptions/{subscription_id}/resourcegroups/{resource_group}" \
                      f"/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{msi_name}"

    # build auth URI for REST API query
    auth_uri = f"{endpoint}?resource=https://vault.azure.net&api-version={api_version}" \
               f"&mi_res_id={msi_resource_id}"

    response = requests.get(url=auth_uri, headers=headers)
    if response.status_code == 500:
        exception = f"Received status code 500, could not retrieve MSI client ID from endpoint\n" \
                    f"Request URI: {auth_uri}"
        logging.error(exception)
        raise Exception(exception)

    return response.json()["client_id"]


def load_json(
    json_str: str
) -> dict:
    """
    Loads a JSON string into a dictionary. Will load JSON with a length = 0 as None
    and will also return None if there is an error loading the JSON

    Args:
        json_str (str): String in JSON format

    Returns:
        dict: JSON as a dictionary
    """
    try:
        json_dict = json.loads(json_str)
    except Exception as ex:
        logging.warning(f"Caught exception: {ex}")
        return None

    if len(json_dict) == 0:
        return None

    return json_dict
