#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, type = int, nargs = '?')
    parser.add_argument('-o', '--offser', dest = 'offset', default = 0, type = int, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -l
    if args.limit is None:
        try:
            args.limit = int(vdjpy.prompt_user('limit'))
        except:
            print 'Not a valid integer. Using default value of 250.'
            args.limit = 250
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        try:
            args.offset = int(vdjpy.prompt_user('offset value'))
        except:
            print 'Not a valid integer. Using default value of 0.'
            args.offset = 0
    kwargs['offset'] = args.offset

    # list permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    permissions = my_agave.files.listPermissions(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(permissions, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in permissions:
            permission_string = item['username'] + ' '
            if item['permission']['read']:
                permission_string += 'r'
            if item['permission']['write']:
                permission_string += 'w'
            if item['permission']['execute']:
                permission_string += 'e'
            print permission_string
