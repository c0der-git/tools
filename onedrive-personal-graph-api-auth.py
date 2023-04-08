# Based on https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python
#from https://github.com/pranabdas/Access-OneDrive-via-Microsoft-Graph-Python

# requirements
import requests
import json
import urllib
import os
from getpass import getpass
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
client_id = os.getenv('CLIENT_ID')
permissions = ['files.read']
response_type = 'token'
redirect_uri = 'http://localhost:8080/'
scope = ''
for items in range(len(permissions)):
    scope = scope + permissions[items]
    if items < len(permissions)-1:
        scope = scope + '+'

print('Click over this link ' +URL + '?client_id=' + client_id + '&scope=' + scope + '&response_type=' + response_type+\
     '&redirect_uri=' + urllib.parse.quote(redirect_uri))
print('Sign in to your account, copy the whole redirected URL.')
code = input("Paste the URL here :")
token = code[(code.find('access_token') + len('access_token') + 1) : (code.find('&token_type'))]
URL = 'https://graph.microsoft.com/v1.0/'
HEADERS = {'Authorization': 'Bearer ' + token}
response = requests.get(URL + 'me/drive/', headers = HEADERS)
if (response.status_code == 200):
    response = json.loads(response.text)
    print('Connected to the OneDrive of', response['owner']['user']['displayName']+' (',response['driveType']+' ).', \
         '\nConnection valid for one hour. Reauthenticate if required.')
elif (response.status_code == 401):
    response = json.loads(response.text)
    print('API Error! : ', response['error']['code'],\
         '\nSee response for more details.')
else:
    response = json.loads(response.text)
    print('Unknown error! See response for more details.')

items = json.loads(requests.get(URL + 'me/drive/root/children', headers=HEADERS).text)
items = items['value']
for entries in range(len(items)):
    print(items[entries]['name'], '| item-id >', items[entries]['id'])
