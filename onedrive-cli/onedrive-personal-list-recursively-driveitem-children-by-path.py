# OneDrive Personal files access with interactive authentification,
# using authority "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"

# *****************************************************************

# List recursively children of a DriveItem with a known path


import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

import datetime
import pytz

# Set the API endpoint and parameters
path = os.getenv('PERS_PATH')
endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:/{path}:/children" #To list OneDrive folder path



params = {
    "select": "id,name,createdDateTime,lastModifiedDateTime,size,file,folder",
    "orderby": "name"
}

# Set the authentication parameters
client_id = os.getenv('PERS_CLIENT_ID')
client_secret = os.getenv('PERS_CLIENT_SECRET')
redirect_uri = os.getenv('PERS_REDIRECT_URI')
scope = "https://graph.microsoft.com/.default"
authorization_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
token_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

# Send a request to the authorization endpoint to obtain an authorization code
auth_params = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scope
}
auth_response = requests.get(authorization_endpoint, params=auth_params)
print("Open this URL in your browser to authorize the application:", auth_response.url)
authorization_code = input("Enter the authorization code from the URL: ")

# Send a request to the token endpoint to obtain an access token
token_params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "code": authorization_code,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
}
token_response = requests.post(token_endpoint, data=token_params)
access_token = json.loads(token_response.text)["access_token"]

# Send a request to the OneDrive API endpoint to retrieve the user's files
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(endpoint, headers=headers, params=params)

# Print the results
print(f"Files in {path}:")
for item in json.loads(response.text)["value"]:
    if item["folder"] is not None:
        # The item is a folder, so make a new request to get the files inside it
        folder_id = item["id"]
        folder_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        folder_response = requests.get(folder_endpoint, headers=headers, params=params)
        print(f"Files in {item['name']}:")
        for file_item in json.loads(folder_response.text)["value"]:
            print(f"- {file_item['name'], file_item['id']}")
    else:
        # The item is a file, so just print its name and ID
        print(f"- {item['name'], item['id']}")