# -----------------------------------------------------
# Import the Workspace and Datastore class
# -----------------------------------------------------
from azureml.core import Workspace, Datastore


# -----------------------------------------------------
# Access the workspace from the config.json 
# -----------------------------------------------------
ws = Workspace.from_config(path="./config")


# -----------------------------------------------------
# Create a datastore 
# -----------------------------------------------------
az_store = Datastore.register_azure_blob_container(
            workspace=ws,
            datastore_name="azure_sdk_blob01",
            account_name="azuremlstbprod",
            container_name="azuremlstb01blob",  
            account_key="8a93HF3znY+FhlkLy9iq4/VKazslmVqrP6NEdX6qnBMOhZ2HyyWL/4275+cdufRIbgA7HcyZFL7I+AStA8hSeQ==")
