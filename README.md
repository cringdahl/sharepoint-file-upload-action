# Sharepoint File Upload Github Action

Uploads one or more files (via glob) to Sharepoint site.

## Variables

The following environment variables & secrets must be defined.

If your full Sharepoint upload path is `https://example.sharepoint.com/sites/mygreatsite/Shared%20Documents/reports/detailed`, the following would be defined:

- `host_name`
  - `'example.sharepoint.com'`
- `site_name`
  - `'mygreatsite'`
- `upload_path`
  - `'reports/detailed'`

You will also need to provide the file or files being sent:

- `file_path`
  - A glob; something like `file.txt` or `*.md`

## Example action.yml

```yml
name: example-file-upload
on: workflow_dispatch
jobs:
  get_report:
    runs-on: ubuntu-latest
    steps:
      - name: Create Test File
        run: touch /tmp/foo.txt
      - name: Send to Sharepoint
        uses: cringdahl/sharepoint-file-upload-action@1.0.0
        with:
          file_path: '*.txt'
          host_name: 'your.sharepoint.com'
          site_name: 'some_site'
          upload_path: 'fake_files'
          sharepoint_token: 'some-token'
          max_retries: optional, default 3
```
