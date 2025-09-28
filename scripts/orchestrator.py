import os
import logging
from utils import load_config
from deploy import deploy_pipeline
from run import run_pipeline
from monitor import monitor_pipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    config = load_config()
    workspace_id = os.getenv("WORKSPACE_ID") or config.get("workspace_id")

    pipelines = [
        {"file": "pipelines/source_prep_pipeline.json", "name": "source_prep_pipeline"},
        {"file": "pipelines/incremental_pipeline.json", "name": "incremental_pipeline"}
    ]

    for pipeline in pipelines:
        logging.info(f"Deploying pipeline: {pipeline['name']}")
        deploy_resp = deploy_pipeline(workspace_id, pipeline["file"], pipeline_name=pipeline["name"])
        pipeline_id = deploy_resp.get("id")

        logging.info(f"Running pipeline: {pipeline['name']}")
        run_resp = run_pipeline(workspace_id, pipeline_id)
        run_id = run_resp.get("id")

        logging.info(f"Monitoring pipeline: {pipeline['name']}")
        success = monitor_pipeline(workspace_id, pipeline_id, run_id)
        if not success:
            logging.error(f"Pipeline {pipeline['name']} failed. Halting orchestrator.")
            exit(1)

    logging.info("All pipelines completed successfully ✅")

if __name__ == "__main__":
    main()
