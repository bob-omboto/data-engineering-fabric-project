import os
import yaml
from deploy import deploy_pipeline

def load_config_file(path: str):
    """Load YAML configuration."""
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    # Workspace ID from environment
    workspace_id = os.getenv("WORKSPACE_ID")
    if not workspace_id:
        raise ValueError("WORKSPACE_ID environment variable is missing.")

    # Load pipelines configuration
    config = load_config_file("configs/pipelines.yml")
    pipelines = config.get("pipelines", [])

    if not pipelines:
        print("No pipelines defined in configuration.")
        return

    for pipeline in pipelines:
        try:
            print(f"Deploying pipeline: {pipeline['name']}")
            deploy_pipeline(
                workspace_id=workspace_id,
                pipeline_file=pipeline["file"],
                pipeline_name=pipeline["name"],
                pipeline_id=pipeline.get("pipeline_id"),
                capacity_object_id=pipeline.get("capacity_object_id")
            )
        except Exception as e:
            print(f"Failed to deploy pipeline {pipeline['name']}: {str(e)}")

if __name__ == "__main__":
    main()
