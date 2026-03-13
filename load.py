import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "erp-raw")
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

def upload_to_blob(local_path, blob_path):
    client = BlobServiceClient.from_connection_string(conn_str)
    container = client.get_container_client(CONTAINER_NAME)
    with open(local_path, "rb") as f:
        container.upload_blob(blob_path, f, overwrite=True)
    print(f"  Uploaded {local_path} → {blob_path}")

def upload_all():
    for root, dirs, files in os.walk("raw"):
        for file in files:
            if file.endswith(".parquet"):
                local_path = os.path.join(root, file)
                blob_path = local_path  # mirrors local structure in blob
                upload_to_blob(local_path, blob_path)

if __name__ == "__main__":
    print("Uploading Parquet files to Azure Blob Storage...")
    upload_all()
    print("Done.")