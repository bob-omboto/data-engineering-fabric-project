import requests
import os
from utils import get_access_token, load_config

def deploy_pipeline(workspace_id: str, pipeline_file: str, pipeline_name: str,
                    pipeline_id: str = None, capacity_object_id: str = None):
    """
    Deploy a pipeline JSON to Microsoft Fabric workspace.

    Args:
        workspace_id: Fabric workspace object ID
        pipeline_file: path to the pipeline JSON file
        pipeline_name: friendly name for the pipeline
        pipeline_id: existing pipeline ID to update (optional)
        capacity_object_id: optional Fabric capacity object ID
    Returns:
        Response JSON from Fabric API
    """
    # Load pipeline JSON
    with open(pipeline_file, "r") as f:
        pipeline_json = load_config(f)  # or json.load(f) if load_config is standard

    # Add optional pipeline metadata
    pipeline_json["name"] = pipeline_name
    if capacity_object_id:
        pipeline_json["capacityObjectId"] = capacity_object_id

    # Get Fabric access token
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Determine endpoint
    if pipeline_id:
        # Update existing pipeline
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/pipelines/{pipeline_id}"
        method = requests.put
    else:
        # Create new pipeline
        url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/pipelines"
        method = requests.post

    # Send request
    response = method(url, headers=headers, json=pipeline_json)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"ERROR: Failed to deploy pipeline {pipeline_name}. Status: {response.status_code}")
        print(response.text)
        raise e

    print(f"Pipeline {pipeline_name} deployed successfully.")
    return response.json()
