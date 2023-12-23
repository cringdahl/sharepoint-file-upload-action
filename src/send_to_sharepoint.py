import sys
import msal
from office365.graph_client import GraphClient
import glob

site_name = sys.argv[1]
sharepoint_host_name = sys.argv[2]
tenant_id = sys.argv[3]
client_id = sys.argv[4]
client_secret = sys.argv[5]
upload_path = sys.argv[6]
file_path = sys.argv[7]

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

def upload_file(self, drive, f, chunk_size=4194304):
    file_size = os.path.getsize(f)
    if file_size < chunk_size:
        return drive.upload_file(f, **kwargs).execute_query()
    else:
       return drive.create_upload_session(
            source_path=f,
            chunk_size=chunk_size,
            chunk_uploaded=progress_status,
            **{'file_size': file_size}
        ).execute_query()

def progress_status(offset, file_size):
    print(f"Uploaded {offset} bytes of {file_size} ... {offset/file_size*100:.2f}%")

for f in local_files:
  try:
    remote_file = upload_file(drive, f)
  except Exception as e:
    print(f"Unexpected error occurred: {e}, {type(e)}")
  finally:
    print(f"File {remote_file.web_url} has been uploaded")