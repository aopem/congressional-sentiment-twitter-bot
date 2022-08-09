import os

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import azure.core.exceptions as e
import twitter_bot.utils.functions as f

class StorageClient:
    def __init__(
        self,
        storage_account_name
    ):
        self.__credential = DefaultAzureCredential(
            managed_identity_client_id=f.get_msi_client_id()
        )
        self.__client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net/",
            credential=self.__credential
        )

    def createContainer(
        self,
        name
    ):
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
        name
    ):
       return self.__client.get_container_client(
            container=name
        )

    def uploadFile(
        self,
        local_filepath,
        container_name
    ):
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
        data_name,
        container_name,
        overwrite=False
    ):
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
        local_filepath,
        container_name
    ):
        filename = os.path.basename(local_filepath)
        container_client = self.__client.get_container_client(
            container=container_name
        )

        with open(local_filepath, "wb") as download_file:
            contents = container_client.download_blob(
                blob=filename
            )
            download_file.write(contents.readall())