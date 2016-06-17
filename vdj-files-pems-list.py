#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, type = int, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', default = 0, type = int, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    project_uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if project_uuid is None:
        sys.exit()

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('file name')
    kwargs['filePath'] = '/projects/' + project_uuid + '/files/' + args.file_name

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
    permissions = my_agave.files.listPermissionsOnDefaultSystem(**kwargs)

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
