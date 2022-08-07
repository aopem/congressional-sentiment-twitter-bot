import json

import twitter_bot.utils.constants as c
from twitter_bot.client.azure import KeyVaultClient


def main():
    secrets = json.load(open(c.SECRETS_FILEPATH))
    azure_config = json.load(open(c.AZURE_CONFIG_FILEPATH))

    print("Creating keyvault client...")
    keyvault = KeyVaultClient(
        key_vault_name=azure_config["resourceGroup"]["resources"]["keyVault"]["name"]
    )

    # now save twitter secrets in key vault
    twitter_secrets = secrets["twitter"]
    for secret_name, secret_value in twitter_secrets.items():
        print(f"Setting {secret_name} to {secret_value}")
        keyvault.setSecret(
            name=secret_name,
            value=secret_value
        )

    return


if __name__ == "__main__":
    main()
