from azure.storage.blob import ContainerClient
import azure.core.exceptions as e

from .azure_storage_broker import AzureStorageBroker

class AzureStorageMgmtBroker(AzureStorageBroker):
    def create_container(
        self,
        name: str
    ) -> ContainerClient:
        """
        Creates a container within an Azure Storage account

        Args:
            name (str): name of container

        Returns:
            ContainerClient: client for interacting with container
        """
        try:
            container = self.__storage_client.create_container(
                name=name
            )
        except e.ResourceExistsError:
            container = self.get_container(
                name=name
            )

        return container

    def get_container(
        self,
        name: str
    ) -> ContainerClient:
        """
        Gets a container client for interacting with a container

        Args:
            name (str): name of container to get

        Returns:
            ContainerClient: _description_
        """
        return self.__storage_client.get_container_client(
            container=name
        )
