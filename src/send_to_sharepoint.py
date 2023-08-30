from dotenv import load_dotenv
import os
import msal
from office365.graph_client import GraphClient
import glob

load_dotenv() # where we keep token info during local dev

site_name = os.environ['SHAREPOINT_SITE_NAME']
sharepoint_host_name = os.environ['SHAREPOINT_HOST_NAME']
tenant_id = os.environ['SHAREPOINT_TENANT_ID']
client_id = os.environ['SHAREPOINT_CLIENT_ID']
client_secret = os.environ['SHAREPOINT_CLIENT_SECRET']
upload_path = os.environ['SHAREPOINT_UPLOAD_PATH']
file_path = os.environ['SHAREPOINT_FILE_PATH']

# below used with 'get_by_url' in GraphClient calls
tenant_url = f'https://{sharepoint_host_name}/sites/{site_name}'

# we're running this in actions, so we'll only ever have one .md file
local_files = glob.glob(file_path)

def acquire_token():
    """
    Acquire token via MSAL
    """
    authority_url = f'https://login.microsoftonline.com/{tenant_id}'
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id=client_id,
        client_credential=client_secret
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token

client = GraphClient(acquire_token)
drive = client.sites.get_by_url(tenant_url).drive.root.get_by_path(upload_path)

for f in local_files:
  try:
    remote_file = drive.upload_file(f).execute_query()
  except Exception as e:
    print(f"Unexpected error occurred: {e}, {type(e)}")
  finally:
    print(f"File {remote_file.web_url} has been uploaded")

