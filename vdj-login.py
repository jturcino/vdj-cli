import json
import requests
from agavepy.agave import Agave

token_url = 'https://vdjserver.org:443/api/v1/token'
username = 
password = 

auth = requests.auth.HTTPBasicAuth(username, password)
resp = requests.post(token_url, auth = auth, verify = False)
resp.raise_for_status()
token_info = resp.json()
token_dict = token_info['result']
token = token_dict['access_token'] # THIS IS ACCESS TOKEN
