from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import src.utils.functions as f

class KeyVaultClient:
    def __init__(
        self,
        key_vault_name: str
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
        name: str,
        value
    ):
        self.__client.set_secret(
            name=name,
            value=value
        )

    def getSecret(
        self,
        name: str
    ):
        return self.__client.get_secret(
            name=name
        )

    def deleteSecret(
        self,
        name: str
    ):
        poller = self.__client.begin_delete_secret(
            name=name
        )
        return poller.result()
