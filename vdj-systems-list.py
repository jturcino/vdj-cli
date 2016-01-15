#!/usr/bin/env python

import json
import os.path
import requests
import argparse
from agavepy.agave import Agave
import sharedfunctions

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
        access_token = sharedfunctions.read_cache('~/.vdjapi', 'access_token')
        if access_token is None:
            access_token = sharedfunctions.prompt_user('access_token')
    else:
        access_token = args.accesstoken

    # get systems 
#    my_agave = Agave(api_server = base_url, token = access_token)
    my_agave = sharedfunctions.make_vdj_agave(base_url, access_token)
    systems = my_agave.systems.list()

    # restrict output (check for storage, execution, default, and/or private only flags)
    if args.storageonly is True:
        systems = sharedfunctions.restrict_systems(systems, 'STORAGE')
    elif args.executiononly is True:
        systems = sharedfunctions.restrict_systems(systems, 'EXECUTION')
    elif args.defaultonly is True:
        systems = sharedfunctions.restrict_systems(systems, 'DEFAULT')
    elif args.privateonly is True:
        systems = sharedfunctions.restrict_systems(systems, 'PRIVATE')

    # if -v
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for system in systems:
            print str(system['id'])
