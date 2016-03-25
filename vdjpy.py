#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import os.path
from datetime import datetime

def create(username, password):
    """Create a new authentication token at url with given username and password."""
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    (access_token, refresh_token) = parse_response(resp)
    if os.path.isfile(os.path.expanduser(user_cache)) is True:
        write_tokens(access_token, refresh_token)
    return (access_token, refresh_token)

def get_dictionary_value(dictionary, key):
    """Returns value of given key for given dictionary"""
    return dictionary[key]

def get_vdj_projects(accesstoken):
    """Hits VDJ projects metadata endpoint. Returns reponse after writing response to projects cache."""
    my_agave = make_vdj_agave(accesstoken)
    projects = my_agave.meta.listMetadata(q = projects_query, limit = 5000, offset = 0)
    write_json(projects, projects_cache)
    return projects

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def make_vdj_agave(access_token):
    """Make an Agave object at url with given access token."""
    if access_token is None:
        access_token = read_json_cache(user_cache, 'access_token')
        if access_token is None:
            access_token = prompt_user('access_token')
    return Agave(api_server = base_url, token = access_token)

def parse_response(resp):
    """Return access and refresh tokens from JSON-generated dictionary."""
    token_info = resp.json()
    token_dict = get_dictionary_value(token_info, 'result')
    access_token = get_dictionary_value(token_dict, 'access_token')
    refresh_token = get_dictionary_value(token_dict, 'refresh_token')
    return (str(access_token), str(refresh_token))

def prompt_user(key):
    """Promp user to enter value for given key at command line."""
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key

def read_for_login(cache, key):
    """Get the value corresponding to key. Defaults to given file, but uses input upon failure."""
    if os.path.isfile(os.path.expanduser(user_cache)) is True:
        json_dict = read_json(cache)
        return str(get_dictionary_value(json_dict, key))
    else:
        return prompt_user(key)

def read_json(filename):
    """Return the contents of a file containing json. Returns None if the file does not exist."""
    if os.path.isfile(os.path.expanduser(filename)) is True:
        with open(os.path.expanduser(filename), 'r') as json_file:
            dictionary = json.load(json_file)
        json_file.close()
        return dictionary
    else:
        return None

def refresh(username, refresh_token):
    """Refresh authentication token at url with given username and refresh token."""
    auth = requests.auth.HTTPBasicAuth(username, refresh_token)
    resp = requests.put(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    (access_token, refresh_token) = parse_response(resp)
    if os.path.isfile(os.path.expanduser(user_cache)) is True:
        write_tokens(access_token, refresh_token)
    return (access_token, refresh_token)

def write_json(json_in, filename):
    """Write the given json to the given file. Changes from unicode to string."""
    with open(os.path.expanduser(filename), 'w') as json_file:
        json.dump(json_in, json_file)
    json_file.close()
    return

def write_tokens(access_token, refresh_token):
    with open(os.path.expanduser(user_cache), 'r') as json_file:
        json_dict = json.load(json_file)
    json_file.close()
    json_dict['access_token'] = unicode(access_token)
    json_dict['refresh_token'] = unicode(refresh_token)
    write_json(json_dict, user_cache)
    return

base_url = 'https://vdj-agave-api.tacc.utexas.edu'
token_url = 'https://vdjserver.org:443/api/v1/token'
projects_query = '{"name":"project"}'
projects_cache = './.vdjprojects'
user_cache = '~/.vdjapi'
