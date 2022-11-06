"""
Script for setting keyvault secrets
"""
import sys
import os
import logging
from azure.core.exceptions import ResourceNotFoundError

# needed to import src functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from twitter_bot.utils.functions import get_secrets_dict
from twitter_bot.brokers import AzureKeyVaultBroker


def main():
    secrets = get_secrets_dict()
    logging.info("Creating AzureKeyVaultBroker...")
    key_vault_broker = AzureKeyVaultBroker()

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
