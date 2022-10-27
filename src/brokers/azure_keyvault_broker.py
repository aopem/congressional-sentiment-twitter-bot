from azure.keyvault.secrets import SecretClient, KeyVaultSecret

from .azure_cloud_broker import AzureCloudBroker

class AzureKeyVaultBroker(AzureCloudBroker):
    def __init__(self, key_vault_name):
        super().__init__()
        self.__key_vault_client = SecretClient(
            vault_url=f"https://{key_vault_name}.vault.azure.net",
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
        self.__key_vault_client.set_secret(
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
        return self.__key_vault_client.get_secret(
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
        poller = self.__key_vault_client.begin_delete_secret(
            name=name
        )
        return poller.result()
