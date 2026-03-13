from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import os

load_dotenv()
conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
print("Connection string found:", conn_str is not None)
client = BlobServiceClient.from_connection_string(conn_str)
client.create_container("erp-raw")
print("Container created.")