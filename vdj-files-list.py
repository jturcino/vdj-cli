#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    kwargs = {}

    # cache and query
    projects_cache = './.vdjprojects'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if uuid is None:
        sys.exit()

    # -l (for listMetadata)
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o (for listMetadata)
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # if args.project exits
    uuid = str(uuid)
    files = vdjpy.get_project_files(uuid, args.accesstoken)
    if args.limit < 5000:
        files = files[:args.limit]

    # if -v
    if args.verbose:
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in files:
            print item['value']['name']
