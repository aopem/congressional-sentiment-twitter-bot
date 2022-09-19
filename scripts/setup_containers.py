"""
Script for setting up needed storage account containers
"""
# needed to import src functions
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import logging
import argparse
from azure.identity import DefaultAzureCredential

import src.utils.constants as c
import src.utils.functions as f
from src.client.azure import StorageClient


def run(
    skips: list
):
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))
    credential = DefaultAzureCredential(
        managed_identity_client_id=f.get_msi_client_id(
            subscription_id=azure_config["subscriptionId"],
            resource_group=azure_config["resourceGroup"]["name"],
            msi_name=azure_config["resourceGroup"]["managedIdentity"]["name"],
            api_version=azure_config["resourceGroup"]["managedIdentity"]["restApiVersion"]
        )
    )

    logging.info("Creating StorageClient...")
    storage_account = StorageClient(
        credential=credential,
        storage_account_name=azure_config["resourceGroup"]["storageAccount"]["name"]
    )

    # create a container for each function in the function app
    for function in azure_config["resourceGroup"]["functionApp"]["functions"]:
        container_name = function.replace("_", "")

        if skips:
            if container_name in skips:
                continue

        logging.info(f"Creating container: {container_name}")
        storage_account.createContainer(
            name=container_name
        )

        # now, add all needed empty container files
        for filename in azure_config["resourceGroup"]["storageAccount"]["containers"][container_name]["emptyFiles"]:
            logging.info(f"Uploading {filename} to container")
            storage_account.uploadData(
                data="",
                data_name=filename,
                container_name=container_name,
                overwrite=True
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--skips',
        nargs='*',
        type=str
    )

    args = parser.parse_args()
    run(args.skips)


if __name__ == "__main__":
    main()
