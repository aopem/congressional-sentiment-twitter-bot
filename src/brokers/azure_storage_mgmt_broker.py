"""
Azure Storage Management Broker class
"""
from azure.storage.blob import ContainerClient
from azure.mgmt.storage import StorageManagementClient
import azure.core.exceptions as e

from .azure_storage_broker import AzureStorageBroker

class AzureStorageMgmtBroker(AzureStorageBroker):
    """
    Class for performing storage management operations

    Attributes:
        __storage_mgmt_client (StorageManagementClient): internal storage
        management client for interacting with Azure
    """
    def __init__(self):
        super().__init__()
        self.__storage_mgmt_client = StorageManagementClient(
            credential=self.authenticate(),
            subscription_id=self._subscription_id
        )

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
