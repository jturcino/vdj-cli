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
    parser.add_argument('-u', '--username', dest = 'username', default = None, nargs = '?')
    args = parser.parse_args()

    # get token
    access_token = vdjpy.read_cache('access_token')
    if access_token is None:
        access_token = vdjpy.prompt_user('access_token')

    # get username
    if args.username is None:
        args.username = vdjpy.read_cache('username')
        if args.username is None:
            args.username = vdjpy.prompt_user('username')

    # get systems
    my_agave = vdjpy.make_vdj_agave(access_token)
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
