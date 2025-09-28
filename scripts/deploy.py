import sys
import logging
from utils import api_post, encode_json_file, FABRIC_BASE_URL, load_config

config = load_config()

def deploy_pipeline(workspace_id, json_path, pipeline_name=None):
    pipeline_name = pipeline_name or config.get("pipeline_name", "MyPipeline")
    payload = {
        "displayName": pipeline_name,
        "type": "DataPipeline",
        "definition": {
            "format": "json",
            "parts": [
                {
                    "path": "pipeline.json",
                    "payload": encode_json_file(json_path)
                }
            ]
        }
    }
    url = f"{FABRIC_BASE_URL}/workspaces/{workspace_id}/items/import"
    response = api_post(url, payload)
    pipeline_id = response.get("id")

    logging.info(f"✅ Pipeline deployed: {pipeline_id}")
    # Export as Azure DevOps variable
    print(f"##vso[task.setvariable variable=PIPELINE_ID]{pipeline_id}")
    return response

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python deploy.py <workspace_id> <pipeline.json>")
        sys.exit(1)
    deploy_pipeline(sys.argv[1], sys.argv[2])
