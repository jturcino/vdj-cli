#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Publish an app for public use. Global admin privileges are required to publish an app.')
    parser.add_argument('-a', '--appID', dest = 'appID', nargs = '?', help = 'application ID')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['body'] = {'action': 'publish'}

    # -a
    if args.appID is None:
	args.appID = vdjpy.prompt_user('app ID')
    kwargs['appId'] = args.appID

    # publish app
    publish = my_agave.apps.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(publish, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully added app', publish['id']
