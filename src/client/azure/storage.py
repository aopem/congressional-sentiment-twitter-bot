import os

from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.identity import DefaultAzureCredential
import azure.core.exceptions as e
import src.utils.functions as f

class StorageClient:
    """
    Client for interacting with Azure Storage account

    Attributes:
        __credential (DefaultAzureCredential): credential to use
        for accessing Azure
        __client (BlobServiceClient): internal client for interacting
        with storage blobs
    """
    def __init__(
        self,
        storage_account_name: str
    ):
        """
        Constructor for StorageClient

        Args:
            storage_account_name (str): name of Azure Storage account
        """
        self.__credential = DefaultAzureCredential(
            managed_identity_client_id=f.get_msi_client_id()
        )
        self.__client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=self.__credential
        )

    def createContainer(
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
            container = self.__client.create_container(
                name=name
            )
        except e.ResourceExistsError:
            container = self.getContainer(
                name=name
            )

        return container

    def getContainer(
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
        return self.__client.get_container_client(
            container=name
        )

    def uploadFile(
        self,
        local_filepath: str,
        container_name: str
    ) -> None:
        """
        Uploads file at local_filepath to container_name

        Args:
            local_filepath (str): local path to file to upload
            container_name (str): name of container to upload file to
        """
        filename = os.path.basename(local_filepath)
        blob_client = self.__client.get_blob_client(
            container=container_name,
            blob=filename
        )

        with open(local_filepath, "rb") as upload_file:
            blob_client.upload_blob(
                data=upload_file
            )

    def uploadData(
        self,
        data,
        data_name: str,
        container_name: str,
        overwrite: bool = False
    ) -> None:
        """
        Uploads data as data_name to container_name

        Args:
            data (Any): data to upload
            data_name (str): name to give data after uploaded
            container_name (str): name of container to upload data to
            overwrite (bool, optional): If true, will overwrite data with data_name
            if data_name already exists in container_name. Defaults to False.
        """
        blob_client = self.__client.get_blob_client(
            container=container_name,
            blob=data_name
        )

        blob_client.upload_blob(
            data=data,
            overwrite=overwrite
        )

    def downloadFile(
        self,
        local_filepath: str,
        container_name: str
    ) -> None:
        """
        Downloads file from from container_name to local_filepath, using
        file name in local_filepath as name of blob to download

        Args:
            local_filepath (str): name of file to download, path to save it to
            container_name (str): name of container to download file from
        """
        filename = os.path.basename(local_filepath)
        container_client = self.__client.get_container_client(
            container=container_name
        )

        with open(local_filepath, "wb") as download_file:
            contents = container_client.download_blob(
                blob=filename
            )
            download_file.write(contents.readall())
