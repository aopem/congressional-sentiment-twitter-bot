import json

import twitter_bot.utils.constants as c
from twitter_bot.client.azure import StorageClient


def main():
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))

    print("Creating StorageClient...")
    storage_account = StorageClient(
        storage_account_name=azure_config["resourceGroup"]["storageAccount"]["name"]
    )

    # create a container for each function in the function app
    for function in azure_config["resourceGroup"]["functionApp"]["functions"]:
        container_name = function.replace("_", "")

        print(f"Creating container: {container_name}")
        storage_account.createContainer(
            name=container_name
        )

    return


if __name__ == "__main__":
    main()
