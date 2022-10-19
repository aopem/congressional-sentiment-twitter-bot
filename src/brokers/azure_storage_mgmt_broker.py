from azure.storage.blob import BlobServiceClient, ContainerClient
import azure.core.exceptions as e

from .azure_cloud_mgmt_broker import AzureCloudMgmtBroker

class AzureStorageMgmtBroker(AzureCloudMgmtBroker):
    def __init__(self):
        super().__init__()
        self.__storage_account_name = self.__config["resourceGroup"]["storageAccount"]["name"]
        self.__storage_account_url = f"https://{self.__storage_account_name}.blob.core.windows.net/"
        self.__storage_client = BlobServiceClient(
            credential=self.authenticate(),
            account_url=self.__storage_account_url
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
