#!/user/bin/env python

import json
import requests
from agavepy.agave import Agave
import os.path
from datetime import datetime
import argparse
import urllib
from operator import itemgetter
from requests.packages.urllib3.exceptions import InsecureRequestWarning # to disable later on

# global constants
base_url = 'https://vdj-agave-api.tacc.utexas.edu'
token_url = 'https://vdjserver.org:443/api/v1/token'
projects_cache = './.vdjprojects'
user_cache = '~/.vdjapi2'
data_url = 'data.vdjserver.org/'

# does not contain parse_response, read_for_login, create, refresh, and write_tokens

def check_for_project_name(json_object, name):
    """Checks for a entries with a given name in a given json dictionary"""
    for item in json_object:
        if item['value']['name'] == name:
            return item['uuid']

def get_dictionary_value(dictionary, key):
    """Returns value of given key for given dictionary"""
    return dictionary[key]

def get_token(username, refresh, password):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if password is None: # refresh token
        auth = requests.auth.HTTPBasicAuth(username, refresh)
        resp = requests.put(token_url, auth = auth, verify = False)
    else: # create token
        auth = requests.auth.HTTPBasicAuth(username, password)
        resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    resp = resp.json()
    return resp

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

def prompt_user(key):
    """Promp user to enter value for given key at command line."""
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key

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

def write_json(json_in, filename):
    """Write the given json to the given file. Changes from unicode to string."""
    with open(os.path.expanduser(filename), 'w') as json_file:
        json.dump(json_in, json_file)
    return


