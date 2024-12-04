from azure.identity import AzureCliCredential

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.storage import StorageManagementClient

import pandas as pd

 

# Initialize Azure CLI credentials

credential = AzureCliCredential()

 

# Azure Subscription ID

subscription_id = "xxxxx-xxxxd01303ec644a"

 

# Initialize clients

resource_client = ResourceManagementClient(credential, subscription_id)

storage_client = StorageManagementClient(credential, subscription_id)

 

# Fetch all Storage Accounts

def get_storage_account_details():

    storage_account_details = []

 

    for resource_group in resource_client.resource_groups.list():

        resource_group_name = resource_group.name

 

        # Fetch storage accounts in the resource group

        storage_accounts = storage_client.storage_accounts.list_by_resource_group(resource_group_name)

 

        for account in storage_accounts:

            # Get detailed properties of the storage account

            account_detail = storage_client.storage_accounts.get_properties(resource_group_name, account.name)

 

            # Extract relevant properties

            sku_name = account.sku.name if account.sku else "Unknown"

            tier = account.sku.tier if account.sku else "Unknown"

            kind = account.kind if account.kind else "Unknown"

            location = account.location if account.location else "Unknown"

            access_tier = account_detail.access_tier if hasattr(account_detail, 'access_tier') else "N/A"

            allow_blob_public_access = account_detail.allow_blob_public_access if hasattr(account_detail, 'allow_blob_public_access') else "N/A"

            minimum_tls_version = account_detail.minimum_tls_version if hasattr(account_detail, 'minimum_tls_version') else "N/A"

            supports_https_traffic_only = account_detail.supports_https_traffic_only if hasattr(account_detail, 'supports_https_traffic_only') else "N/A"

            encryption_key_source = account_detail.encryption.key_source if hasattr(account_detail, 'encryption') else "N/A"

            provisioning_state = account_detail.provisioning_state if hasattr(account_detail, 'provisioning_state') else "N/A"

            primary_location = account_detail.primary_location if hasattr(account_detail, 'primary_location') else "N/A"

            status_of_primary = account_detail.status_of_primary if hasattr(account_detail, 'status_of_primary') else "N/A"

 

            # Add details to the list

            storage_account_details.append({

                "Name": account.name,

                "Resource Group": resource_group_name,

                "Type": account.type,

                "SKU Name": sku_name,

                "Tier": tier,

                "Kind": kind,

                              "Access Tier": access_tier

               

            })

 

    return storage_account_details

 

# Save data to Excel

def save_to_excel(data, file_name="storage_account_details.xlsx"):

    df = pd.DataFrame(data)

    df.to_excel(file_name, index=False)

    print(f"Data saved to {file_name}")

 

# Main Execution

if __name__ == "__main__":

    storage_account_details = get_storage_account_details()

    save_to_excel(storage_account_details)

 