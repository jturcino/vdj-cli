#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import argparse

def parse_response(resp):
    token_info = resp.json()
    token_dict = token_info['result']
    access_token = token_dict['access_token']
    refresh_token = token_dict['refresh_token']
    return (str(access_token), str(refresh_token))

def create(token_url,username, password):
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

def refresh(token_url, username, refresh_token):
    auth = requests.auth.HTTPBasicAuth(username, refresh_token)
    resp = requests.put(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', dest = 'username')
parser.add_argument('-p', '--password', dest = 'password')
parser.add_argument('-r', '--refresh', dest = 'refresh')
args = parser.parse_args()

token_url = 'https://vdjserver.org:443/api/v1/token'

if args.refresh != None:
    (access_token, refresh_token) = refresh(token_url, args.username, args.refresh)

else:
    (access_token, refresh_token) = create(token_url, args.username, args.password)

print 'Access token is:', access_token
print 'Refresh token is:', refresh_token
