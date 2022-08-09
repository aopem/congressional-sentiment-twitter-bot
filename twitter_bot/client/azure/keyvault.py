from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import twitter_bot.utils.functions as f

class KeyVaultClient:
    def __init__(
        self,
        key_vault_name
    ):
        self.__credential = DefaultAzureCredential(
            managed_identity_client_id=f.get_msi_client_id()
        )
        self.__client = SecretClient(
            vault_url=f"https://{key_vault_name}.vault.azure.net",
            credential=self.__credential
        )

    def setSecret(
        self,
        name,
        value
    ):
        self.__client.set_secret(
            name=name,
            value=value
        )

    def getSecret(
        self,
        name
    ):
        return self.__client.get_secret(
            name=name
        )

    def deleteSecret(
        self,
        name
    ):
        poller = self.__client.begin_delete_secret(
            name=name
        )
        return poller.result()
