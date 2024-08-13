from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

# Replace with your Key Vault name
KEY_VAULT_NAME = 'thisdicekeyvault'

# Form the Key Vault URL
KEY_VAULT_URL = f'https://{KEY_VAULT_NAME}.vault.azure.net'

def list_secrets():
    # Create a credential object using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create a SecretClient using the Key Vault URL and credential
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

    try:
        # List all secrets in the Key Vault
        secrets = client.list_properties_of_secrets()

        for secret in secrets:
            # Retrieve the value of each secret
            secret_name = secret.name
            secret_value = client.get_secret(secret_name).value
            print(f"Name: {secret_name}, Value: {secret_value}")

    except ResourceNotFoundError:
        print("Key Vault or Secret not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_secrets()
