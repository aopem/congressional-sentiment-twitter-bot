"""
Azure Key Vault Client class
"""
from azure.keyvault.secrets import SecretClient, KeyVaultSecret
from azure.identity import DefaultAzureCredential

class KeyVaultClient:
    """
    Client for interacting with Azure Key Vault

    Attributes:
        __client (Secret Client): internal client for interacting
        with key vault secrets
    """
    def __init__(
        self,
        credential: DefaultAzureCredential,
        key_vault_name: str
    ):
        """
        Constructor for KeyVaultClient

        Args:
            credential (DefaultAzureCredential): credential object for Azure authentication
            key_vault_name (str): name of key vault to access
        """
        self.__client = SecretClient(
            vault_url=f"https://{key_vault_name}.vault.azure.net",
            credential=credential
        )

    def setSecret(
        self,
        name: str,
        value
    ) -> None:
        """
        Set the value of secret "name" to "value"

        Args:
            name (str): name of secret
            value (Any): value of secret
        """
        self.__client.set_secret(
            name=name,
            value=value
        )

    def getSecret(
        self,
        name: str
    ) -> KeyVaultSecret:
        """
        Gets secret identified by "name"

        Args:
            name (str): name of secret

        Returns:
            KeyVaultSecret: secret from key vault
        """
        return self.__client.get_secret(
            name=name
        )

    def deleteSecret(
        self,
        name: str
    ):
        """
        Deletes secret identified by "name"

        Args:
            name (str): name of secret

        Returns:
            Any: status of deletion
        """
        poller = self.__client.begin_delete_secret(
            name=name
        )
        return poller.result()
