from azure.mgmt.resource import ResourceManagementClient
from .azure_cloud_broker import AzureCloudBroker

class AzureCloudMgmtBroker(AzureCloudBroker):
    def __init__(self):
        super().__init__()
        self.__resource_mgmt_client = ResourceManagementClient(
            credential=self.authenticate(),
            subscription_id=self.__subscription_id
        )
