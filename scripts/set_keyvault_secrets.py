"""
Script for setting keyvault secrets
"""
# needed to import src functions
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import logging
import azure.core.exceptions as e
from azure.identity import DefaultAzureCredential

import src.utils.constants as c
import src.utils.functions as f
from src.client.azure import KeyVaultClient


def main():
    secrets = f.get_secrets_dict()
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))
    credential = DefaultAzureCredential(
        managed_identity_client_id=f.get_msi_client_id(
            subscription_id=azure_config["subscriptionId"],
            resource_group=azure_config["resourceGroup"]["name"],
            msi_name=azure_config["resourceGroup"]["managedIdentity"]["name"],
            api_version=azure_config["resourceGroup"]["managedIdentity"]["restApiVersion"]
        )
    )
    key_vault_name = azure_config["resourceGroup"]["keyVault"]["name"]

    logging.info("Creating KeyVaultClient...")
    keyvault = KeyVaultClient(
        credential=credential,
        key_vault_name=key_vault_name
    )

    # now save secrets in key vault, if not already there
    for secret_name, secret_value in secrets.items():
        try:
            keyvault.getSecret(
                name=secret_name
            )
            logging.info(f"Secret {secret_name} already exists in {key_vault_name}")

        except e.ResourceNotFoundError:
            logging.info(f"Setting {secret_name} to {secret_value}")
            keyvault.setSecret(
                name=secret_name,
                value=secret_value
            )


if __name__ == "__main__":
    main()
