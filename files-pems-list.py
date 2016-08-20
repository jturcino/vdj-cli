#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'List permissions for a file or directory on a remote system. System defaults to data.vdjserver.org.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, type = int, nargs = '?', help = 'maximum number of results return')
    parser.add_argument('-o', '--offset', dest = 'offset', default = 0, type = int, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
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
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
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
