# Fabric Pipeline Deployer

Automated deployment, execution, monitoring, and archiving of **Microsoft Fabric pipelines** via REST API and Azure DevOps CI/CD.

---

## **Project Overview**

This repository contains scripts and configuration for:

- Deploying Fabric pipelines from JSON templates
- Running pipelines programmatically
- Monitoring pipeline execution status
- Archiving run metadata and outputs to Azure Blob Storage
- Full CI/CD automation with Azure DevOps

---

## **Project Structure**

fabric_pipeline_deployer/
│
├── pipelines/ # Pipeline JSON templates
│ └── my_pipeline.json
├── scripts/ # Python scripts
│ ├── deploy.py
│ ├── run.py
│ ├── monitor.py
│ └── utils.py
├── configs/ # Environment-specific settings
│ └── settings.yaml
├── requirements.txt
└── azure-pipelines.yml # CI/CD pipeline

yaml
Copy code

---

## **Prerequisites**

- Python 3.9+  
- Azure DevOps account with pipeline permissions  
- Azure Blob Storage account for archiving  
- Fabric workspace access and API permissions
- Entra ID Service Principal for authentication

---

## **Setup**

1. **Clone the repo**

```bash```
git clone <repo-url>
cd fabric_pipeline_deployer

2. Install dependencies

```bash```
Copy code
pip install -r requirements.txt

3. Configure environment variables / secrets

- In Azure DevOps, create a Variable Group FabricSecrets with:

    . AZURE_CLIENT_ID

    . AZURE_CLIENT_SECRET

    . TENANT_ID

- Add AZURE_STORAGE_CONN as a secret for Blob Storage access.

- Update configs/settings.yaml with:

    . workspace_id

    . pipeline_name

    . timeout_minutes

    . poll_interval_seconds

    . retry_attempts

Usage
Deploy a pipeline
```bash```
python scripts/deploy.py <workspace_id> pipelines/my_pipeline.json

Run the pipeline
```bash```
python scripts/run.py <workspace_id> <pipeline_id>

Monitor the pipeline
```bash```
python scripts/monitor.py <workspace_id> <pipeline_id> <run_id>

The deploy.py and run.py scripts automatically set Azure DevOps pipeline variables (PIPELINE_ID, RUN_ID) for CI/CD integration.

CI/CD (Azure DevOps)
- Pipeline automatically triggers on commits to main.

- Steps:

    1. Install Python dependencies

    2. Deploy pipeline to Fabric

    3. Trigger pipeline execution

    4. Monitor run until completion

    5. Archive run metadata to Blob Storage

- azure-pipelines.yml supports:

    1. Variable groups for secrets

    2. Inline variables for workspace IDs

    3. Logging, retry, and timeout handling

- Production Best Practices
    Store all pipeline JSON templates in Git (version control).

    Never hardcode secrets; use Azure DevOps Library or Key Vault.

    Use separate configs for dev, staging, and prod environments.

    Enable monitoring and logging for each pipeline run.

    Archive all pipeline metadata and outputs for compliance.

    Use retry and timeout logic to handle transient API errors.

License
This project is licensed under MIT License.