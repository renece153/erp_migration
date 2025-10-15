from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


def get_key_vault_secrets(_secret_name):
    tenant_id = "91aaadf7-17fe-4e27-8046-10d35b53e9eb"
    client_id = "d993c5aa-27a6-44ac-9728-32e944aab947"
    client_secret = "wN68Q~o4jvAxdS3nKwHehT~Eihe_sPeq_U5QMctv"
    vault_url = "https://erpteam-keyvault.vault.azure.net/"
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(_secret_name)
    return secret.value


def get_nested_value(data, path):
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

