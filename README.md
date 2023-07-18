# gdrive3

Google Drive as blob storage an extension of [PyDrive2](https://docs.iterative.ai/PyDrive2/quickstart/)

## Service Account Authentication

1. Create a [new project](https://console.cloud.google.com/cloud-resource-manager)
2. Search for `google drive api` and enable it
3. Create [credentials](https://console.cloud.google.com/apis/credentials) for an OAuth client for your project

   1. Select ‘Application type’ to be Web application.
   2. Enter an appropriate name.
   3. Input http://localhost:8080/ for ‘Authorized redirect URIs’.
   4. Click ‘Create’.
4. Copy your client_id and client_secret values

Once you have your client_id and client_secret values, rename `.sample-env` to `.env` and add your client_id and client_secret

Run `python init.py`

1. Follow the one time auth flow. 
2. Navigate to the created credentials file
   1. Windows: ..../AppData/Local/pydrive2fs/...
   2. Mac: ...
3. Copy the .json file contents 