#!/usr/bin/env python

import argparse
import json
import os.path
from agavepy.agave import Agave
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appID', dest = 'appID', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, nargs = '?', type = int)
    parser.add_argument('-o', '--offset', dest = 'offset', default = 0, nargs = '?', type = int)
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    kwargs = {}

    # check appID
    if args.appID is None:
        args.appID = vdjpy.prompt_user('app ID')
    kwargs['appId'] = args.appID

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_list = my_agave.apps.listPermissions(**kwargs)

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
            print item['username'], user_pems
