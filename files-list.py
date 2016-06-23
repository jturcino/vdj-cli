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
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o 
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # get files
    files = my_agave.files.list(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in files:
            print item['name']
