#!/user/bin/env python

import json
import requests
from agavepy.agave import Agave
import os.path
from os import listdir
from datetime import datetime
import argparse
import urllib
from operator import itemgetter
from requests.packages.urllib3.exceptions import InsecureRequestWarning # to disable later on

# global constants
base_url = 'https://vdj-agave-api.tacc.utexas.edu'
token_url = 'https://vdjserver.org:443/api/v1/token'
projects_cache = './.vdjprojects'
user_cache = '~/.vdjapi'
data_url = 'data.vdjserver.org/'

def build_vdj_path(project_uuid, file_name, filetype, extra_path):
    """Build vdj path to file based on whether the file is a projecFile or projectJobFile"""
    path = '/projects/' + project_uuid
    if filetype == 'projectJobFile':
	path += '/analyses/'
    else:
	path += '/files/'
    path += extra_path + file_name
    return path

def check_for_project_name(json_object, name):
    """Checks for a entries with a given name in a given json dictionary"""
    for item in json_object:
        if str(item['value']['name']) == name:
            return item['uuid']
    return None

def get_dictionary_value(dictionary, key):
    """Returns value of given key for given dictionary"""
    return dictionary[key]

def get_file_metadata(files_list, file_name):
    """Returns the vdj metadata for a file"""
    files_names = ''
    for item in files_list:
        if item['value']['name'] == file_name:
            return item
        files_names += item['value']['name'] + '\n'
    print 'The file', file_name, 'does not exist. \nHere are your current files: \n' + files_names
    return None

def get_project_files(uuid, filetype, kwargs, agave_object):
    kwargs['q'] = '{"name": ' 
    if filetype is None:
        kwargs['q'] += '{ $in: ["projectFile", "projectJobFile"]}'
    else:
        kwargs['q'] += '"' + filetype + '"'
    kwargs['q'] += ', "value.projectUuid": "' + uuid + '", "value.isDeleted": false}'
    files = agave_object.meta.listMetadata(**kwargs)
    return files

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

def get_uuid(project_name, agave_object):
    uuid = None
    if os.path.isfile(os.path.expanduser(projects_cache)) is True:
        projects = read_json(projects_cache)
        uuid = check_for_project_name(projects, project_name)
    if uuid is None:
        kwargs = {'limit': 5000, 'offset': 0}
        projects = get_vdj_projects(agave_object, kwargs)
        uuid = check_for_project_name(projects, project_name)
    if uuid is None:
        print 'The project', project_name, 'does not exist. \nHere are your current projects and uuids:'
        for item in projects:
            print item['value']['name'] + ' ' + item['uuid']
    return uuid

def get_vdj_projects(agave_object, kwargs):
    """Hits VDJ projects metadata endpoint. Returns reponse after writing response to projects cache."""
    kwargs['q'] = '{"name":"project"}'
    projects = agave_object.meta.listMetadata(**kwargs)
    write_json(projects, projects_cache)
    return projects

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def make_vdj_agave(accesstoken):
    """Make an Agave object at url with given access token."""
    if accesstoken is None:
        dictionary = read_json(user_cache)
        if dictionary is None:
            accesstoken = prompt_user('access_token')
        else:
            accesstoken = dictionary['access_token']
    return Agave(api_server = base_url, token = accesstoken)

def prompt_for_integer(key, default_value):
    return_value = default_value
    try:
        return_value = int(prompt_user(key))
    except:
        print 'Not a valid integer. Using default value of', str(default_value) + '.'
    return return_value

def prompt_user(key):
    """Prompt user to enter value for given key at command line."""
    print 'Enter', key.replace('_', ' ') + ':',
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

def recursive_file_upload(filepath, destfilepath, systemID, agave_object, verbose):
    """Recursively upload contents of a directory. Prints verbose or concise output as files are uploaded. No metadata updates."""
    filename = os.path.basename(filepath)
    if destfilepath[len(destfilepath) - 1] != '/':
        destfilepath += '/'
    if os.path.isdir(filepath) is True:
        mkdir = agave_object.files.manage(systemId = systemID,
                                  filePath = destfilepath,
                                  body = {'action': 'mkdir',
                                          'path': filename})
        if verbose:
            print json.dumps(mkdir, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        else:
            print 'Made directory', filename, 'at path', destfilepath
        destfilepath += filename + '/'
        for item in os.listdir(filepath):
            recursive_file_upload(filepath + '/' + item, destfilepath, systemID, agave_object, verbose)
    else:
        file_upload = agave_object.files.importData(systemId = systemID,
                                      filePath = destfilepath,
                                      fileToUpload = open(filepath),
                                      fileName = filename)
        if verbose:
            print json.dumps(file_upload, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        else:
            print 'Uploaded', filename, 'to', destfilepath
        return

def update_metadata(project_uuid, file_name, file_uuid, extras):
    metadata_path = '/vdjZ/projects/' + project_uuid + '/files/' + file_name
    metadata_url = 'https://vdjserver.org/api/v1/notifications/files/import?fileUuid=' + file_uuid + '&path=' + metadata_path + '&projectUuid=' + project_uuid + extras
    resp = requests.post(metadata_url)
    resp.raise_for_status()
    return resp.json()

def write_json(json_in, filename):
    """Write the given json to the given file. Changes from unicode to string."""
    with open(os.path.expanduser(filename), 'w') as json_file:
        json.dump(json_in, json_file)
    return
