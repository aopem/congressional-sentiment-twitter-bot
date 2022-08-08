import json
import azure.core.exceptions as e

import twitter_bot.utils.constants as c
import twitter_bot.utils.functions as func
from twitter_bot.client.azure import KeyVaultClient


def main():
    secrets = func.get_secrets_dict()
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))

    print("Creating KeyVaultClient...")
    keyvault = KeyVaultClient(
        key_vault_name=azure_config["resourceGroup"]["keyVault"]["name"]
    )

    # now save twitter secrets in key vault, if not already there
    twitter_secrets = secrets["twitter"]
    for secret_name, secret_value in twitter_secrets.items():
        try:
            keyvault.getSecret(
                name=secret_name
            )

        except e.ResourceNotFoundError:
            print(f"Setting {secret_name} to {secret_value}")
            keyvault.setSecret(
                name=secret_name,
                value=secret_value
            )

    return


if __name__ == "__main__":
    main()
