#!/usr/bin/env python

import argparse
import json
import os.path
from agavepy.agave import Agave
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appID', dest = 'appID', required = True)
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        args.accesstoken = vdjpy.read_cache('access_token')
        if args.accesstoken is None:
            args.accesstoken = vdjpy.prompt_user('access_token')

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_list = my_agave.apps.listPermissions(appId = args.appID)

    # if -v
    if args.verbose is True:
        print json.dumps(pems_list, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in pems_list:
            user_pems = ''
            if item['permission']['read'] is True:
                user_pems+='r'
            if item['permission']['write'] is True:
                user_pems+='w'
            if item['permission']['execute'] is True:
                user_pems+='x'
            print item['username'] + ': ' + user_pems
