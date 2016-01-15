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
    args = parser.parse_args()

    # get token
    access_token = vdjpy.read_cache('access_token')
    if access_token is None:
        access_token = vdjpy.prompt_user('access_token')

    # get systems
    my_agave = vdjpy.make_vdj_agave(access_token)
    apps = my_agave.apps.list() # flag in here

    # if -v
    if args.verbose is True:
        print apps

    # if no args
    else:
        for app in apps:
            print str(app['id'])
