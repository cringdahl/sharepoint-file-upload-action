import sys
import os
import msal
from office365.graph_client import GraphClient
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.internal.paths.url import UrlPath
from office365.onedrive.driveitems.uploadable_properties import DriveItemUploadableProperties
from office365.runtime.odata.v4.upload_session_request import UploadSessionRequest
from office365.runtime.queries.upload_session import UploadSessionQuery
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

def progress_status(offset, file_size):
    print(f"Uploaded {offset} bytes from {file_size} bytes ... {offset/file_size*100:.2f}%")

def upload_file(drive, local_path, chunk_size):
    file_size = os.path.getsize(local_path)
    if file_size < chunk_size:
        return drive.upload_file(local_path).execute_query()
    else:
        def _start_upload():
            with open(local_path, 'rb') as local_file:
                request = UploadSessionRequest(local_file, chunk_size, (lambda offset: progress_status(offset, file_size)))
                request.execute_query(query)

        file_name = os.path.basename(local_path)
        drive_item = DriveItem(drive.context, UrlPath(file_name, drive.resource_path))
        drive_item_properties = DriveItemUploadableProperties(name=file_name)
        query = UploadSessionQuery(drive_item, {"item": drive_item_properties})
        print(f"file_name: {file_name}, file_size: {file_size}, drive_resource_path: {drive.resource_path}, drive_item: {drive_item}, drive_item_properties: {drive_item_properties}, query: {query}")
        drive.context.add_query(query).after_query_execute(_start_upload)
        return drive_item.get().execute_query()

for f in local_files:
  try:
    remote_file = upload_file(drive, f, 4 * 1024 * 1024)
  except Exception as e:
    print(f"Unexpected error occurred: {e}, {type(e)}")
  finally:
    print(f"File {remote_file.web_url} has been uploaded")
