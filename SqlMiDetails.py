from azure.identity import AzureCliCredential

from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.sql import SqlManagementClient

import pandas as pd

 

# Initialize Azure CLI credentials

credential = AzureCliCredential()

 

# Azure Subscription ID

subscription_id = "xxxxx-xxxxd01303ec644a"

 

# Initialize clients

resource_client = ResourceManagementClient(credential, subscription_id)

sql_client = SqlManagementClient(credential, subscription_id)

 

# Define a mapping for hardware generation descriptions

hardware_generation_map = {

    "Gen5": "Standard-series (Gen 5) - Intel Broadwell, 5.1 GB RAM/vCore",

    "Premium": "Premium-series - Intel Ice Lake, 7 GB RAM/vCore, up to 560 GB",

    "Premium_Memory_Optimized": "Premium-series - memory optimized - Intel Ice Lake, 13.6 GB RAM/vCore, up to 870.4 GB"

}

 

# Fetch all SQL Managed Instances

def get_sql_managed_instances():

    sql_mi_details = []

 

    # Iterate through all resource groups

    for resource_group in resource_client.resource_groups.list():

        resource_group_name = resource_group.name

 

        # Fetch SQL MIs in the resource group

        sql_mis = sql_client.managed_instances.list_by_resource_group(resource_group_name)

 

        for sql_mi in sql_mis:

            # Fetch detailed instance properties

            sql_mi_detail = sql_client.managed_instances.get(resource_group_name, sql_mi.name)

 

            # Extract hardware generation description

            hardware_generation = sql_mi.sku.family if hasattr(sql_mi.sku, 'family') else "Unknown"

            hardware_description = hardware_generation_map.get(hardware_generation, "Custom/Unknown Configuration")

 

            # Extract TLS version

            minimal_tls_version = sql_mi_detail.minimal_tls_version if hasattr(sql_mi_detail, 'minimal_tls_version') else "Unknown"

 

            # Extract storage account type (backup redundancy)

            storage_account_type = sql_mi_detail.storage_account_type if hasattr(sql_mi_detail, 'storage_account_type') else "Unknown"

 

            # Extract zone redundancy

            zone_redundant = "Yes" if getattr(sql_mi_detail, 'zone_redundant', False) else "No"

 

            # Add SQL MI details

            sql_mi_details.append({

                "SQL MI Name": sql_mi.name,

                "Resource Group": resource_group_name,

                "Type": sql_mi.type,

                "Service Tier": sql_mi.sku.tier,

                "Hardware Generation": hardware_description,

                "vCores": sql_mi.sku.capacity,

                "Storage in GB": sql_mi.storage_size_in_gb,

                "Minimal TLS Version": minimal_tls_version,

                "Backup Storage Redundancy": storage_account_type,

                "Zone Redundant": zone_redundant,

            })

 

    return sql_mi_details

 

# Save data to Excel

def save_to_excel(data, file_name="sql_mi_details.xlsx"):

    df = pd.DataFrame(data)

    df.to_excel(file_name, index=False)

    print(f"Data saved to {file_name}")

 

# Main Execution

if __name__ == "__main__":

    sql_mi_details = get_sql_managed_instances()

    save_to_excel(sql_mi_details)