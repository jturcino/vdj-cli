#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import os.path
from datetime import datetime

def create(token_url, username, password):
    """Create a new authentication token at url with given username and password."""
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def make_vdj_agave(access_token):
    """Make an Agave object at url with given access token."""
    if access_token is None:
        access_token = read_cache(cache, 'access_token')
        if access_token is None:
            access_token = prompt_user('access_token')
    return Agave(api_server = base_url, token = access_token)

def parse_response(resp):
    """Return access and refresh tokens from JSON-generated dictionary."""
    token_info = resp.json()
    token_dict = token_info['result']
    access_token = token_dict['access_token']
    refresh_token = token_dict['refresh_token']
    return (str(access_token), str(refresh_token))

def prompt_user(key):
    """Promp user to enter value for given key at command line."""
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key

def read_cache(cache, key):
    """Get the value corresponding to key. Defaults to given file, but uses input upon failure."""
    if os.path.isfile(os.path.expanduser(cache)) is True:
        with open(os.path.expanduser(cache), 'r') as json_file:
            json_dict = json.load(json_file)
        json_file.close()
        return str(json_dict[key])
    else:
        print 'No cache found'
        return None

def refresh(token_url, username, refresh_token):
    """Refresh authentication token at url with given username and refresh token."""
    auth = requests.auth.HTTPBasicAuth(username, refresh_token)
    resp = requests.put(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

def restrict_systems(systems_list, system_type):
    """Remove systems from list that are not of the desired type."""
    new_list = []
    for item in range(0, len(systems_list) - 1):
        if systems_list[item]['type'] == system_type:
            new_list.append(systems_list[item])
    return new_list

def write_cache(access_token, refresh_token):
    """Replace access and refresh tokens in cache with current versions."""
    if os.path.isfile(os.path.expanduser(cache)) is True:
        with open(os.path.expanduser(cache), 'r') as json_file:
            json_dict = json.load(json_file)
        json_file.close()
        json_dict['access_token'] = unicode(access_token)
        json_dict['refresh_token'] = unicode(refresh_token)
        with open(os.path.expanduser(cache), 'w') as json_file:
            json.dump(json_dict, json_file)
        json_file.close()
    return

base_url = 'https://vdj-agave-api.tacc.utexas.edu'
cache = '~/.vdjapi'
