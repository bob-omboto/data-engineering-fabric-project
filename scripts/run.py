import sys
import logging
from utils import api_post, FABRIC_BASE_URL, load_config

config = load_config()

def run_pipeline(workspace_id, pipeline_id):
    url = f"{FABRIC_BASE_URL}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/run"
    response = api_post(url, {})
    run_id = response.get("id")

    logging.info(f"✅ Run started: {run_id}")
    # Export as Azure DevOps variable
    print(f"##vso[task.setvariable variable=RUN_ID]{run_id}")
    return response

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run.py <workspace_id> <pipeline_id>")
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2])
