#!/usr/bin/env python

import json
import os.path
import requests
import argparse
from agave.agavepy import Agave
import pprint

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
    parser.add_argument('-V', '--VeryVerbose', required = False, dest = 'very_verbose', default = False, nargs = '?')
    args = parser.parse_args()

    # url
    base_url = 'https://vdj-agave-api.tacc.utexas.edu'

    # get token
    token = read_cache('~/.vdjapi', 'access_token')
    if token is None:
        token = prompt_user('access_token')
    
    # get systems 
    header = {'Authorization':'Bearer '+token}
    resp = requests.get(url, headers=header)# instead use my_agave = .... then agave.systems.list
    resp.raise_for_status()
    systems = resp.json() 

    # if no args
    if args.very_verbose is False:
        for system in systems['result']:
            print str(system['id'])

    # if -V
    if args.very_verbose is not False:
        pprint.pprint(systems)
