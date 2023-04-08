# OneDrive Personal files access with interactive authentification,
# using authority "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"

import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

import datetime
import calendar

from collections import defaultdict

# Set the API endpoint and parameters
path = os.getenv('PERS_PATH')
endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:/{path}:/children" #To list OneDrive folder path



params = {
    "select": "id,name,createdDateTime,lastModifiedDateTime,size,file,childCount,folder",
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
# Group the files by their createdDateTime
files_by_month = defaultdict(list)
for item in json.loads(response.text)["value"]:
    if item["folder"] is not None:
        print(f"{item['name']}:")
        subfolder_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{item['id']}/children"
        subfolder_response = requests.get(subfolder_endpoint, headers=headers, params=params)
        subfolder_files = json.loads(subfolder_response.text)["value"]
        for file in subfolder_files:
            created_date = datetime.datetime.fromisoformat(file["createdDateTime"][:19]).date()
            files_by_month[(created_date.year, created_date.month)].append(file)

# Print the files grouped by month
for month, files in sorted(files_by_month.items()):
    print(f"\n{calendar.month_name[int(month[1])]}, {month[0]}")
    #print(f"\n{calendar.month_name[int(month.split('-')[1])]}, {month.split('-')[0]}")
    for file in files:
        print(f"- {file['name']}")