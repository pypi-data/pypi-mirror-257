
# cli/main.py
from azure.storage.blob import BlobServiceClient
import argparse
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient

FILE_EXTENSION = [".html", ".xml", ".xls", ".json", ".xlsx", ".csv"]
RFP_CONNECTION_STRING=os.environ.get("RFP_CONNECTION_STRING")

class AzureBlobFileUploader:
    
    _local_file_path: str
    _rfp_file_container: str
    _rfp_blob_name:str
    # _databases: dict = {
    #     "quantum": "rfpmetrics\coverity\quantum",
    #     "mercury": "rfpmetrics\coverity\mercury"
    # }

    def __init__(self , local_file_path: str,blob_name:str, container_name:str):
        print("Intializing AzureBlobFileUploader")
        self._local_file_path = local_file_path
        self._rfp_file_container = container_name
        self._rfp_blob_name=blob_name
    
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(RFP_CONNECTION_STRING)

    def upload_all_files_in_folder(self):
        # Get all files with html extension and exclude directories

        for file_name in os.listdir(self._local_file_path):
            if os.path.isfile(os.path.join(self._local_file_path, file_name)):
                for extension in FILE_EXTENSION:
                    if file_name.endswith(extension):
                        file_content_setting = ContentSettings(content_type=extension[1:])
                        folder_name=self._rfp_blob_name
                        blob_name=f"{folder_name}/{file_name[:-1 * len(extension)]}"
                        blob_client = self.blob_service_client.get_blob_client(container=self._rfp_file_container,
                                                                               blob=blob_name+ extension)
                        print(f"uploading file - {file_name}")
                        with open(os.path.join(self._local_file_path, file_name), "rb") as data:
                            blob_client.upload_blob(data, overwrite=True, content_settings=file_content_setting)

def main():
    parser = argparse.ArgumentParser(description='Upload data to Azure Blob Storage.')
    parser.add_argument("-b", '--blob_name', required=True, help='Name of the blob')
    parser.add_argument("-f", '--local_file_path', required=True, help='Local file path to upload')
    container_name = "rfpmetrics"
    args = parser.parse_args()
    azure_blob_file_uploader=AzureBlobFileUploader(str(args.local_file_path), str(args.blob_name),container_name)
    azure_blob_file_uploader.upload_all_files_in_folder()
    print(f'Uploaded {args.local_file_path} to Azure Blob Storage as {args.blob_name}')

if __name__ == '__main__':
    main()
    

