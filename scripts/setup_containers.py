import json
import argparse

import src.utils.constants as c
from src.client.azure import StorageClient


def run(
    skips: list
):
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))

    print("Creating StorageClient...")
    storage_account = StorageClient(
        storage_account_name=azure_config["resourceGroup"]["storageAccount"]["name"]
    )

    # create a container for each function in the function app
    for function in azure_config["resourceGroup"]["functionApp"]["functions"]:
        container_name = function.replace("_", "")

        if skips:
            if container_name in skips:
                continue

        print(f"Creating container: {container_name}")
        storage_account.createContainer(
            name=container_name
        )

        # now, add all needed empty container files
        for filename in azure_config["resourceGroup"]["storageAccount"]["containers"][container_name]["emptyFiles"]:
            print(f"Uploading {filename} to container")
            storage_account.uploadData(
                data="",
                data_name=filename,
                container_name=container_name,
                overwrite=True
            )

    return


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
