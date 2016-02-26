#!/usr/bin/env python

import argparse
import json
import os.path
from agavepy.agave import Agave
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    parser.add_argument('-P', '--publiconly', dest = 'publiconly', default = False, action = 'store_true')
    parser.add_argument('-Q', '--privateonly', dest = 'privateonly', default = False, action = 'store_true')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, nargs = '?')
#    parser.add_argument('-o', '--offset', dest = 'offset', default = 0, nargs = '?')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        args.accesstoken = vdjpy.read_cache('access_token')
        if args.accesstoken is None:
            args.accesstoken = vdjpy.prompt_user('access_token')
    
    # limit/offset
    print args.limit
    if args.limit is None:
        args.limit = vdjpy.prompt_user('number of apps to return')

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # public/private only
    if args.publiconly is True and args.privateonly is False:
        apps = my_agave.apps.list(publicOnly = args.publiconly, limit = args.limit)
    elif args.privateonly is True and args.publiconly is False:
        apps = my_agave.apps.list(privateOnly = 'true', limit = args.limit)
    else:
        apps = my_agave.apps.list(limit = args.limit)

    # if -v
    if args.verbose is True:
        print json.dumps(apps, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for app in apps:
            print str(app['id'])
