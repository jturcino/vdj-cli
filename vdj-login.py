#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('username')
parser.add_argument('password')
args = parser.parse_args()

token_url = 'https://vdjserver.org:443/api/v1/token'

auth = requests.auth.HTTPBasicAuth(args.username, args.password)
resp = requests.post(token_url, auth = auth, verify = False)
resp.raise_for_status()

token_info = resp.json()
token_dict = token_info['result']
token = token_dict['access_token'] # THIS IS ACCESS TOKEN
print 'The token for username', args.username, 'is:', str(token)