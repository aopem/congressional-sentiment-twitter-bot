import json
import azure.core.exceptions as e

import twitter_bot.utils.constants as c
import twitter_bot.utils.functions as f
from twitter_bot.client.azure import KeyVaultClient


def main():
    secrets = f.get_secrets_dict()
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))

    print("Creating KeyVaultClient...")
    key_vault_name = azure_config["resourceGroup"]["keyVault"]["name"]
    keyvault = KeyVaultClient(
        key_vault_name=key_vault_name
    )

    # now save secrets in key vault, if not already there
    for secret_name, secret_value in secrets.items():
        try:
            keyvault.getSecret(
                name=secret_name
            )
            print(f"Secret {secret_name} already exists in {key_vault_name}")

        except e.ResourceNotFoundError:
            print(f"Setting {secret_name} to {secret_value}")
            keyvault.setSecret(
                name=secret_name,
                value=secret_value
            )

    return


if __name__ == "__main__":
    main()
