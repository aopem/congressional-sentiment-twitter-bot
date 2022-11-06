"""
Script for setting keyvault secrets
"""
import sys
import os
import json
import logging
from azure.core.exceptions import ResourceNotFoundError

# needed to import twitter_bot functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from twitter_bot.brokers import AzureKeyVaultBroker
from twitter_bot.utils.constants import AZURE_CONFIG_FILEPATH

def get_secrets_dict(
    key_vault_broker: AzureKeyVaultBroker
) -> dict:
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

    # get secrets from keyvault and build dict
    secrets_dict = {}
    for secret_name in azure_config["resourceGroup"]["keyVault"]["secrets"]:
        secret = key_vault_broker.get_secret(
            name=secret_name
        )
        secrets_dict[secret_name] = secret.value

    return secrets_dict


def main():
    logging.info("Creating AzureKeyVaultBroker, obtaining secrets to upload...")
    key_vault_broker = AzureKeyVaultBroker()
    secrets = get_secrets_dict(
        key_vault_broker=key_vault_broker
    )

    # now save secrets in key vault, if not already there
    for secret_name, secret_value in secrets.items():
        try:
            key_vault_broker.get_secret(
                name=secret_name
            )
            logging.info(f"Secret {secret_name} already exists in Key Vault")

        except ResourceNotFoundError:
            logging.info(f"Setting {secret_name} to {secret_value}")
            key_vault_broker.set_secret(
                name=secret_name,
                value=secret_value
            )


if __name__ == "__main__":
    main()
