import json
from os.path import exists
import constants as c
from twitter_bot.client.azure import KeyVaultClient


def get_secrets_dict():
    secrets_dict = {}
    if exists(c.SECRETS_FILEPATH):
        secrets_dict = json.load(c.SECRETS_FILEPATH)
    else:
        azure_config = json.load(c.AZURE_CONFIG_FILEPATH)
        keyvault = KeyVaultClient(
            key_vault_name=azure_config["resourceGroup"]["resources"]["keyVault"]["name"]
        )

        # get secrets from keyvault and build dict
        for secret_name in azure_config["resourceGroup"]["keyVault"]["secretNames"]:
            secret = keyvault.getSecret(
                name=secret_name
            )
            secrets_dict["twitter"][secret_name] = secret.value

    return secrets_dict
