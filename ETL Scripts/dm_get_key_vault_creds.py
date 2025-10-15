from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient


def get_key_vault_secrets(_secret_name):
    tenant_id = "Redacted"
    client_id = "Redacted"
    client_secret = "Redacted"
    vault_url = "Redacted"
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


