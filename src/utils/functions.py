import os
import json
import logging

import src.client.azure as azclient
from .constants import *


def get_secrets_dict() -> dict:
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
    azure_config = json.load(open(AZURE_CONFIG_FILEPATH))

    msi_client_id = os.getenv(f"{azure_config['resourceGroup']['managedIdentity']['clientId']}")
    if not msi_client_id:
        exception = "Could not retrieve MSI client ID\n"
        exception += f"os.environ = {os.environ}"
        logging.error(exception)
        raise Exception(exception)

    return msi_client_id


def load_json(
    json_str: str
) -> dict:
    try:
        json_dict = json.loads(json_str)
    except Exception as e:
        logging.warn(f"Caught exception: {e}")
        return None

    if len(json_dict) == 0:
        return None

    return json_dict
