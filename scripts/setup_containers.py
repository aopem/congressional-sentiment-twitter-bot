"""
Script for setting up needed storage account containers
"""
import sys
import os
import json
import logging
import argparse

# needed to import src functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from twitter_bot_func_app.brokers import AzureStorageBroker, AzureStorageMgmtBroker
from twitter_bot_func_app.utils.constants import AZURE_CONFIG_FILEPATH


def run(
    skips: list
):
    azure_config = json.load(open(AZURE_CONFIG_FILEPATH))

    logging.info("Creating AzureStorageBroker, AzureStorageMgmtBroker...")
    storage_broker = AzureStorageBroker()
    storage_mgmt_broker = AzureStorageMgmtBroker()

    # create a container for each function in the function app
    for function in azure_config["resourceGroup"]["functionApp"]["functions"]:
        container_name = function.replace("_", "")

        if skips:
            if container_name in skips:
                continue

        logging.info(f"Creating container: {container_name}")
        storage_mgmt_broker.create_container(
            name=container_name
        )

        # now, add all needed empty container files
        for filename in azure_config["resourceGroup"]["storageAccount"]["containers"][container_name]["emptyFiles"]:
            logging.info(f"Uploading {filename} to container")
            storage_broker.upload_data(
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
