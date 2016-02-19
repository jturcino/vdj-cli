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
    parser.add_argument('-P', '--publiconly', dest = 'publiconly', default = '', action = 'store_true')
    parser.add_argument('-Q', '--privateonly', dest = 'privateonly', default = '', action = 'store_true')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        args.accesstoken = vdjpy.read_cache('access_token')
        if args.accesstoken is None:
            args.accesstoken = vdjpy.prompt_user('access_token')

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # public/private only
    if args.publiconly is True:
        args.publiconly = 'true'
    if args.privateonly is True:
        args.privateonly = 'true'
    apps = my_agave.apps.list(publicOnly = args.publiconly, privateOnly = args.privateonly)

    # if -v
    if args.verbose is True:
        print json.dumps(apps, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for app in apps:
            print str(app['id'])
