# Example of interactive authentification for MS Graph API, Business Account
# Don't work for Personal Account. Fails with error: 'Tenant does not have a SPO license.'

import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv
load_dotenv()

# Set the required variables
client_id = os.getenv('CLIENT_ID')
tenant_id = os.getenv('TENANT_ID')
redirect_uri = os.getenv('REDIRECT_URI')
scopes = ['https://graph.microsoft.com/.default']

# Set up the authentication using MSAL
app = PublicClientApplication(client_id=client_id, authority='https://login.microsoftonline.com/' + tenant_id)
result = app.acquire_token_silent(scopes=scopes, account=None)

if not result:
    flow = app.initiate_device_flow(scopes=scopes)
    print(flow['message'])
    result = app.acquire_token_by_device_flow(flow)
    print(result)

if 'access_token' not in result:
    print('Access token not found in result. Authentication failed.')
    exit()

# Get the list of files and folders in the root of OneDrive
headers = {'Authorization': 'Bearer ' + result['access_token']}
url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print('Failed to get the content of the root of OneDrive. Status code:', response.status_code)
    print(response.json())
    exit()

response_json = response.json()

for item in response_json['value']:
    print(item['name'])
