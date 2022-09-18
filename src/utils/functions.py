"""
Miscellaneous utility functions
"""
import os
import json
import logging

import src.client.azure as azclient
from .constants import *


def get_secrets_dict() -> dict:
    """
    Obtains a dictionary of all the required secrets. Uses secrets.json if running locally,
    otherwise uses the configured Azure Key Vault

    Returns:
        dict: dictionary object containing all secrets listed in keyvault.secrets from the
        Azure config file
    """
    secrets_dict = {}
    if LOCAL_EXECUTION:
        secrets_dict = json.load(open(SECRETS_FILEPATH))
    else:
        azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
        keyvault = azclient.KeyVaultClient(
            key_vault_name=azure_config["resourceGroup"]["keyVault"]["name"]
        )

        # get secrets from keyvault and build dict
        for secret_name in azure_config["resourceGroup"]["keyVault"]["secrets"]:
            secret = keyvault.getSecret(
                name=secret_name
            )
            secrets_dict[secret_name] = secret.value

    return secrets_dict


def get_msi_client_id() -> str:
    """
    Gets the MSI client ID for the identity in the Azure config file

    Raises:
        Exception: Indicates the MSI client ID could not be obtained

    Returns:
        str: MSI client ID string
    """
    azure_config = json.load(open(AZURE_CONFIG_FILEPATH))

    # TODO: clean up, currently testing
    subscription_id = azure_config["subscriptionId"]
    resource_group = azure_config["resourceGroup"]["name"]
    msi_name = azure_config["resourceGroup"]["managedIdentity"]["name"]
    msi_auth_endpoint = os.getenv("IDENTITY_ENDPOINT")
    x_identity_header = {"X-IDENTITY-HEADER": os.getenv("IDENTITY_HEADER")}
    resource_uri = f"https://{azure_config['resourceGroup']['functionApp']['name']}.azurewebsites.net"
    api_version = "2019-08-01"
    auth_uri = f"{msi_auth_endpoint}?resource={resource_uri}&api-version={api_version}"

    msi_resource_id = f"/subscriptions/{subscription_id}/resourcegroups/{resource_group}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{msi_name}"
    auth_uri += f"&mi_res_id={msi_resource_id}"
    # NOTE: end of testing

    r = requests.get(url=auth_uri, headers=x_identity_header)
    print(r)
    msi_client_id = r["client_id"]

    # msi_client_id = os.getenv(f"{azure_config['resourceGroup']['managedIdentity']['clientId']}")
    if not msi_client_id:
        exception = "Could not retrieve MSI client ID\n"
        exception += f"os.environ = {os.environ}"
        logging.error(exception)
        raise Exception(exception)

    return msi_client_id


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
    except Exception as e:
        logging.warn(f"Caught exception: {e}")
        return None

    if len(json_dict) == 0:
        return None

    return json_dict
