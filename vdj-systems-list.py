#!/usr/bin/env python

import json
import os.path
import requests
import argparse
from agavepy.agave import Agave

def read_cache(file_path, key):
    """Get the value corresponding to key. Defaults to given file, but uses input upon failure."""
    if os.path.isfile(os.path.expanduser(file_path)) is True:
        with open(os.path.expanduser(file_path), 'r') as json_file:
            json_dict = json.load(json_file)
        json_file.close()
        return str(json_dict[key])
    else:
        print 'No cache found'
        return None

def prompt_user(key):
    """Prompt user to enter value for given key at command line."""
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key

def restrict_systems(systems_list, system_type):
    """Remove systems from list that are not of the desired type."""
    new_list = []
    for item in range(0, len(systems_list) - 1):
        if systems_list[item]['type'] == system_type:
            new_list.append(systems_list[item])
    return new_list

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    parser.add_argument('-S', '--storageonly', dest = 'storageonly', action = 'store_true')
    parser.add_argument('-E', '--executiononly', dest = 'executiononly', action = 'store_true')
    parser.add_argument('-D', '--defaultonly', dest = 'defaultonly', action = 'store_true')
    parser.add_argument('-Q', '--privateonly', dest = 'privateonly', action = 'store_true')
    args = parser.parse_args()

    # url
    base_url = 'https://vdj-agave-api.tacc.utexas.edu'

    # get token
    if args.accesstoken is None:
        access_token = read_cache('~/.vdjapi', 'access_token')
        if access_token is None:
            access_token = prompt_user('access_token')
    else:
        access_token = args.accesstoken

    # get systems 
    my_agave = Agave(api_server = base_url, token = access_token)
    systems = my_agave.systems.list()

    # restrict output (check for storage, execution, default, and/or private only flags)
    if args.storageonly is True:
        systems = restrict_systems(systems, 'STORAGE')
    elif args.executiononly is True:
        systems = restrict_systems(systems, 'EXECUTION')
    elif args.defaultonly is True:
        systems = restrict_systems(systems, 'DEFAULT')
    elif args.privateonly is True:
        systems = restrict_systems(systems, 'PRIVATE')

    # if -v
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for system in systems:
            print str(system['id'])
