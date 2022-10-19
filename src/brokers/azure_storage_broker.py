import os
from azure.storage.blob import BlobServiceClient

from .azure_cloud_broker import AzureCloudBroker

class AzureStorageBroker(AzureCloudBroker):
    def __init__(self):
        super().__init__()
        self.__storage_account_name = self.__config["resourceGroup"]["storageAccount"]["name"]
        self.__storage_account_url = f"https://{self.__storage_account_name}.blob.core.windows.net/"
        self.__storage_client = BlobServiceClient(
            credential=self.authenticate(),
            account_url=self.__storage_account_url
        )

    def upload_file(
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
        blob_client = self.__storage_client.get_blob_client(
            container=container_name,
            blob=filename
        )

        with open(local_filepath, "rb") as upload_file:
            blob_client.upload_blob(
                data=upload_file
            )

    def upload_data(
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
        blob_client = self.__storage_client.get_blob_client(
            container=container_name,
            blob=data_name
        )

        blob_client.upload_blob(
            data=data,
            overwrite=overwrite
        )

    def download_file(
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
        container_client = self.__storage_client.get_container_client(
            container=container_name
        )

        with open(local_filepath, "wb") as download_file:
            contents = container_client.download_blob(
                blob=filename
            )
            download_file.write(contents.readall())
