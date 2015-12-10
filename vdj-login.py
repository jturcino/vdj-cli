#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username',dest = 'username')
parser.add_argument('-p', '--password',dest = 'password')
parser.add_argument('-r', '--refresh', dest = 'refresh token')
args = parser.parse_args()

token_url = 'https://vdjserver.org:443/api/v1/token'

# add ifs for username
if args.refresh:
	auth = requests.auth.HTTPBasicAuth(args.username, args.refresh)
	resp = requests.put(token_url, auth = auth, verify = False)

else:
	auth = requests.auth.HTTPBasicAuth(args.username, args.password)
	resp = requests.post(token_url, auth = auth, verify = False)

	resp.raise_for_status()

	token_info = resp.json()
	token_dict = token_info['result']
	access_token = token_dict['access_token'] # THIS IS ACCESS TOKEN
	refresh_token = token_dict['refresh_token'] # THIS IS REFRESH TOKEN
	print 'The access token for username', args.username, 'is:', str(access_token)
	print 'The refresh token for username', args.username, 'is:', str(refresh_token)