import os
import json
import base64
import time
import logging
import requests
import yaml
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FABRIC_BASE_URL = "https://api.fabric.microsoft.com/v1"

def load_config(config_path="configs/settings.yaml"):
    """Load environment-specific configuration"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_access_token():
    """Get Fabric API access token via Azure Identity"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://api.fabric.microsoft.com/.default")
    return token.token

def api_post(url, body, retries=3, backoff=5):
    """POST request with retry logic"""
    for attempt in range(1, retries+1):
        try:
            token = get_access_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(backoff)
            else:
                raise

def api_get(url, retries=3, backoff=5):
    """GET request with retry logic"""
    for attempt in range(1, retries+1):
        try:
            token = get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(backoff)
            else:
                raise

def encode_json_file(path):
    """Base64 encode JSON for Fabric import"""
    with open(path, "r") as f:
        return base64.b64encode(f.read().encode("utf-8")).decode("utf-8")

def upload_to_blob(storage_connection_string, container_name, file_name, content):
    """
    Upload string content to Azure Blob Storage
    """
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Create container if it doesn't exist
    try:
        container_client.create_container()
    except Exception:
        pass  # already exists

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    blob_name = f"{file_name}_{timestamp}.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(content, overwrite=True)
    logging.info(f"Uploaded run info to blob: {blob_name}")
    return blob_name
