import os
from azure.identity import ClientSecretCredential

def get_access_token():
    """ Authenticate using Azure DevOps Key Vault secrets:
    TenantID, ClientID, ClientSecret
    """
    tenant_id = os.getenv("TenantID")
    client_id = os.getenv("ClientID")
    client_secret = os.getenv("ClientSecret")

    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("One or more authentication secrets are missing from environment variables.")

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret
    )
    token = credential.get_token("https://api.fabric.microsoft.com/.default")
    return token.token
