import sys
import time
import json
import logging
from utils import api_get, FABRIC_BASE_URL, load_config, upload_to_blob

config = load_config()
STORAGE_CONN = None
CONTAINER = "fabric-pipeline-archive"

def monitor_pipeline(workspace_id, pipeline_id, run_id):
    timeout = config.get("timeout_minutes", 60) * 60
    interval = config.get("poll_interval_seconds", 15)
    start_time = time.time()

    global STORAGE_CONN
    STORAGE_CONN = STORAGE_CONN or os.getenv("AZURE_STORAGE_CONN")
    if not STORAGE_CONN:
        logging.warning("AZURE_STORAGE_CONN not set. Run metadata will not be archived.")

    while True:
        run_status = api_get(f"{FABRIC_BASE_URL}/workspaces/{workspace_id}/dataPipelines/{pipeline_id}/runs/{run_id}")
        status = run_status.get("status")
        logging.info(f"Pipeline run {run_id} status: {status}")

        if status in ["Succeeded", "Failed", "Cancelled"]:
            if STORAGE_CONN:
                upload_to_blob(STORAGE_CONN, CONTAINER, f"pipeline_{pipeline_id}_run_{run_id}", json.dumps(run_status))
            if status == "Succeeded":
                logging.info("Pipeline completed successfully ✅")
                return True
            else:
                logging.error(f"Pipeline ended with status: {status}")
                return False

        if time.time() - start_time > timeout:
            logging.error("Pipeline monitoring timed out ⏱️")
            if STORAGE_CONN:
                upload_to_blob(STORAGE_CONN, CONTAINER, f"pipeline_{pipeline_id}_run_{run_id}_timeout", json.dumps(run_status))
            return False

        time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python monitor.py <workspace_id> <pipeline_id> <run_id>")
        sys.exit(1)
    monitor_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])
