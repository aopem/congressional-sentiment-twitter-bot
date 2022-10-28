"""
Azure Key Vault Broker class
"""
from azure.keyvault.secrets import SecretClient, KeyVaultSecret

from .azure_cloud_broker import AzureCloudBroker

class AzureKeyVaultBroker(AzureCloudBroker):
    """
    Class for performing Azure Key Vault operations

    Args:
        _key_vault_name (str): name of key vault
        _vault_url (str): URL of key vault
        _key_vault_client (SecretClient): client for interacting
        with key vault secrets
    """
    def __init__(self):
        super().__init__()
        self._key_vault_name = self._config["resourceGroup"]["keyVault"]["name"]
        self._vault_url = f"https://{self._key_vault_name}.vault.azure.net"
        self._key_vault_client = SecretClient(
            vault_url=self._vault_url,
            credential=self.authenticate()
        )

    def set_secret(
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
        self._key_vault_client.set_secret(
            name=name,
            value=value
        )

    def get_secret(
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
        return self._key_vault_client.get_secret(
            name=name
        )

    def delete_secret(
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
        poller = self._key_vault_client.begin_delete_secret(
            name=name
        )
        return poller.result()
