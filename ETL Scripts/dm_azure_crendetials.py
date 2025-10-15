




import os
import requests

# Set your credentials (replace with actual values or use environment variables)
# HCP_CLIENT_ID = os.getenv("HCP_CLIENT_ID", "your-client-id")
# HCP_CLIENT_SECRET = os.getenv("HCP_CLIENT_SECRET", "your-client-secret")

# Step 1: Get the HCP API token
auth_url = "https://auth.idp.hashicorp.com/oauth2/token"
auth_payload = {
"client_id": "Bodrtu2LYKx1NtMwjNEmmwEGN74lzoZZ",
"client_secret": "cTHmCz4aQDFDvaQdqUPd6mTM3Y2idho_qdFlaGVE3J491Lk94zsa5T80ZyuL8V6V",
"grant_type": "client_credentials",
"audience": "https://api.hashicorp.cloud"
}

auth_response = requests.post(auth_url, data=auth_payload)
auth_response.raise_for_status()
access_token = auth_response.json()["access_token"]

# Step 2: Use the token to fetch secrets
secrets_url = "https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/a026813b-5b8e-4aa5-b8c5-b69c3ce4363b/projects/f4c06206-0d20-4034-9a9f-6c4f76191e03/apps/data-migration-secrets/secrets:open"

headers = {
"Authorization": f"Bearer {access_token}"
}

secrets_response = requests.get(secrets_url, headers=headers)
secrets_response.raise_for_status()
secrets = secrets_response.json()

# Print the secrets
print("Fetched secrets:", secrets)
