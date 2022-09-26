import os
import azure.cosmos.cosmos_client as cosmos_client
from utils.config import config
from azure.storage.blob import BlobServiceClient, ContainerClient, __version__
from azure.cosmos.partition_key import PartitionKey


class Database:
    def __init__(self, conn_str=config['azure_storage_connection_string']):
        self.conn_str = conn_str
        self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
        self.blob_client = None

        try:
            print("Azure Blob Storage: v" + __version__)

        except Exception as ex:
            print('Exception: '+str(ex))

        self.cosmosclient = cosmos_client.CosmosClient(config["azure_cosmos"]["account_url"], config["azure_cosmos"]["account_key"])
        self.cosmosdb = self.cosmosclient.create_database_if_not_exists(config["azure_cosmos"]["db_name"])
        self.cosmoscontainer = self.cosmosdb.create_container_if_not_exists(config["azure_cosmos"]["con_name"], PartitionKey(path=config["azure_cosmos"]["part_key"], kind='Hash'))

        try:
            print("Azure Cosmos DB: "+ str(self.cosmosclient))
        
        except Exception as ex:
            print('Exception: '+str(ex))

    def set_container(self, name):
        blob_client = ContainerClient.from_connection_string(config['azure_storage_connection_string'], name)
        if blob_client.exists():
            self.blob_client = blob_client
        else:
            self.blob_client = self.blob_service_client.create_container(name)
        print("Selected container: " + self.blob_client.container_name)

    def upload_blob(self, blobname, file):
        try:
            with open(file, 'rb') as data:
                blob = self.blob_client.upload_blob(blobname, data)
            self.upload_blob_reference(blobname, blob.url)
            return blob.url

        except Exception as ex:
            print('Load fail: '+str(ex))
    
    def upload_blob_reference(self, id, reference):
        try:
            item = self.cosmoscontainer.read_item(id, id.split("+")[0])
            new_item = item
            new_item.update({"frame": reference})
            self.cosmoscontainer.replace_item(item, new_item)

        except:
            item = self.cosmoscontainer.create_item(
                {
                    "id": id,
                    "cam": id.split("+")[0],
                    "datetime": None, 
                    "sensor1": None,
                    "sensor2": None,
                    "sensor3": None,
                    "frame": reference
                }
            )
