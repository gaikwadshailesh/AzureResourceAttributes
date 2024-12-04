**Azure Resource Cost Insights**


This simple project provides Python scripts to extract detailed information about Azure resources, 
specifically SQL Managed Instances and Storage Accounts, which impact Azure cost management. The data includes information such as service tiers, SKUs, storage details, and other critical properties, allowing you to analyze cost-driving factors effectively.

This is just a sample project you can extend the code base depending on your requirement. 

Prerequisites
Python 3.7 or higher
Azure CLI authenticated with the appropriate subscription (az login)
Required Python modules:
azure-identity
azure-mgmt-resource
azure-mgmt-sql
azure-mgmt-storage
pandas


Install them using:
bash
Copy code
pip install azure-identity azure-mgmt-resource azure-mgmt-sql azure-mgmt-storage pandas
