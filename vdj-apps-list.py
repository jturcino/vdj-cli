#!/usr/bin/env python

import argparse
import json
import os.path
from agavepy.agave import Agave
import sharedfunctions
from bson import json_util

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # url
    base_url = 'https://vdj-agave-api.tacc.utexas.edu'

    # path to information cache
    vdj_cache = '~/.vdjapi'

    # get token
    access_token = sharedfunctions.read_cache(vdj_cache, 'access_token')
    if access_token is None:
        access_token = sharedfunctions.prompt_user('access_token')

    # get systems
#    my_agave = Agave(api_server = base_url, token = access_token)
    my_agave = sharedfunctions.make_vdj_agave(base_url, access_token)
    apps = my_agave.apps.list()

    # if -v
    if args.verbose is True:
        print json.dumps(apps, default=json_util.default)
#        for index in range(0, len(apps) - 1):
#            apps[index]['lastModified'] = str(apps[index]['lastModified'])
#        print json.dumps(apps, sort_keys = True, indent = 4, separators = (',', ': '))
##        print apps[0]['lastModified']
##        print apps[0]['lastModified'].strftime('%m/%d/%Y')

    # if no args
    else:
        for app in apps:
            print str(app['id'])
