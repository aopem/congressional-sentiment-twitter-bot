import json
import logging

import twitter_bot.client.azure as azclient
from .constants import *


def get_secrets_dict():
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


def get_msi_client_id():
    msi_client_id = None
    if not LOCAL_EXECUTION:
        azure_config = json.load(open(AZURE_CONFIG_FILEPATH))
        msi_client_id = azure_config["resourceGroup"]["managedIdentity"]["clientId"]

    return msi_client_id


def load_json(
    json_str: str
):
    try:
        json_dict = json.loads(json_str)
    except Exception as e:
        logging.warn(f"Caught exception: {e}")
        return None

    if len(json_dict) == 0:
        return None

    return json_dict