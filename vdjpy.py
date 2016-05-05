#!/usr/bin/env python

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning # to disable later on
from agavepy.agave import Agave
import os.path
from datetime import datetime
from operator import itemgetter

# global constants
base_url = 'https://vdj-agave-api.tacc.utexas.edu'
token_url = 'https://vdjserver.org:443/api/v1/token'
projects_cache = './.vdjprojects'
user_cache = '~/.vdjapi'
data_url = 'data.vdjserver.org/'

def check_for_project_name(json_object, name):
    """Checks for a entries with a given name in a given json dictionary"""
    for item in json_object:
        if item['value']['name'] == name:
            return item['uuid']

def get_dictionary_value(dictionary, key):
    """Returns value of given key for given dictionary"""
    return dictionary[key]

def get_uuid(project_name, accesstoken):
    uuid = None
    if os.path.isfile(os.path.expanduser(projects_cache)) is True:
        projects = read_json(projects_cache)
        uuid = check_for_project_name(projects, project_name)
    else:
        projects = get_vdj_projects(accesstoken, 5000, 0)
        uuid = check_for_project_name(projects, project_name)
    if uuid is None:
        print 'The project', project_name, 'does not exist. \nHere are your current projects and uuids:'
        for item in projects:
            print item['value']['name'] + ' ' + item['uuid']
    return str(uuid)

def get_vdj_projects(accesstoken, limit_in, offset_in):
    """Hits VDJ projects metadata endpoint. Returns reponse after writing response to projects cache."""
    projects_query = '{"name":"project"}'
    my_agave = make_vdj_agave(accesstoken)
    projects = my_agave.meta.listMetadata(q = projects_query, limit = limit_in, offset = offset_in)
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
        dictionary = read_json(user_cache)
        if dictionary is None:
            access_token = prompt_user('access_token')
        else:
            access_token = dictionary['access_token']
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
    dictionary = read_json(cache)
    if dictionary is None:
        return prompt_user(key)
    else:
        return str(dictionary[key])

def read_json(filename):
    """Return the contents of a file containing json. Returns None if the file does not exist."""
    if os.path.isfile(os.path.expanduser(filename)) is True:
        with open(os.path.expanduser(filename), 'r') as json_file:
            try:
                dictionary = json.load(json_file)
                return dictionary
            except ValueError:
                print "JSON could not be parsed in " + filename
    return None

def sortbyquery(mylist, query):
    """Sorts a list of dictionaries with the given query"""
    if query is None:
        query = prompt_user("key by which to sort")
    if query == 'value.name':
        mylist.sort(key = lambda e: e['value']['name'])
    else:
        mylist.sort(key = itemgetter(query))
    return mylist

def create(username, password):
    """Create a new authentication token at url with given username and password."""
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    (access_token, refresh_token) = parse_response(resp)
    if os.path.isfile(os.path.expanduser(user_cache)) is True:
        write_tokens(access_token, refresh_token)
    return (access_token, refresh_token)

def refresh(username, refresh_token):
    """Refresh authentication token at url with given username and refresh token."""
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
    """Updates access and refresh tokens before writing them to user_cache"""
    with open(os.path.expanduser(user_cache), 'r') as json_file:
        json_dict = json.load(json_file)
    json_file.close()
    json_dict['access_token'] = unicode(access_token)
    json_dict['refresh_token'] = unicode(refresh_token)
    write_json(json_dict, user_cache)
    return

