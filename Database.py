import os
from utils.config import config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


class Database:
    def __init__(self, conn_str=config['azure_storage_connection_string']):
        self.conn_str = conn_str
        self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_str)
        self.blob_client = None

        try:
            print("Azure Blob Storage v" + __version__)

        except Exception as ex:
            print('Exception: '+ex)

    def set_container(self, name):
        blob_client = ContainerClient.from_connection_string(config['azure_storage_connection_string'], name)
        if blob_client.exists():
            self.blob_client = blob_client
        else:
            self.blob_client = self.blob_service_client.create_container(name)
        print("Selected container: " + self.blob_client.container_name)

    def upload_blob(self, blobname, file):
        with open(file, 'rb') as data:
            self.blob_client.upload_blob(blobname, data)
