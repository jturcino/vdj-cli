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
    """Promp user to enter value for given key at command line."""
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key



if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-S', '--storageonly', dest = 'storageonly', action = 'store_true')
    parser.add_argument('-E', '--executiononly', dest = 'executiononly', action = 'store_true')
    parser.add_argument('-D', '--defaultonly', dest = 'defaultonly', action = 'store_true')
    parser.add_argument('-Q', '--privateonly', dest = 'privateonly', action = 'store_true')

    args = parser.parse_args()

    # url
    base_url = 'https://vdj-agave-api.tacc.utexas.edu'

    # get token
    access_token = read_cache('~/.vdjapi', 'access_token')
    if access_token is None:
        access_token = prompt_user('access_token')

    # get systems 
    my_agave = Agave(api_server = base_url, token = access_token)
    systems = my_agave.systems.list()

    # restrict output (check for storage, execution, default, and/or private only flags)
    for item in range(0, len(systems)-1):
        if systems[item]['type'] is not THING:
            del systems[item]





    # if -v
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for system in systems:
            print str(system['id'])
