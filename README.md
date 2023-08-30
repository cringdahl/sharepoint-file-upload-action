# Sharepoint File Upload Github Action

Uploads one or more files (via glob) to Sharepoint site.

## Variables
The following environment variables & secrets must be defined. 

If your full Sharepoint upload path is `https://example.sharepoint.com/sites/mygreatsite/Shared%20Documents/reports/detailed`, the following would be defined:

* `SHAREPOINT_HOST_NAME`
  * `'example.sharepoint.com'`
* `SHAREPOINT_SITE_NAME`
  * `'mygreatsite'`
* `SHAREPOINT_UPLOAD_PATH`
  * `'reports/detailed'`


The following will be provided to you by your Sharepoint administrator when you ask for a client ID. A reminder: _put secrets in **Settings/Security/Secrets and variables/Actions**_

* `SHAREPOINT_TENANT_ID`
* `SHAREPOINT_CLIENT_ID`
* `SHAREPOINT_CLIENT_SECRET`

