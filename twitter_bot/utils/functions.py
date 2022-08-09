import json
from os.path import exists
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError

from twitter_bot.client.azure import KeyVaultClient
from .constants import *


def get_secrets_dict():
    secrets_dict = {}
    if exists(SECRETS_FILEPATH):
        secrets_dict = json.load(open(SECRETS_FILEPATH))
    else:
        azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
        keyvault = KeyVaultClient(
            key_vault_name=azure_config["resourceGroup"]["keyVault"]["name"]
        )

        # get secrets from keyvault and build dict
        for secret_name in azure_config["resourceGroup"]["keyVault"]["secrets"]:
            secret = keyvault.getSecret(
                name=secret_name
            )
            secrets_dict[secret_name] = secret.value

    return secrets_dict


def azure_authenticate():
    credential = None
    try:
        credential = DefaultAzureCredential()
    except ClientAuthenticationError:
        azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
        credential = DefaultAzureCredential(
            managed_identity_client_id=azure_config["resourceGroup"]["managedIdentity"]["clientId"]
        )

    return credential