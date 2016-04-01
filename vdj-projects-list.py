#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # query and cache
    query = '{"name":"project"}'
    projects_cache = './.vdjprojects'

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_user('project limit')

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_user('offset value')

    # make object
    projects = vdjpy.get_vdj_projects(args.accesstoken)

    # if -v
    if args.verbose is True:
        print json.dumps(projects, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
       for item in projects:
           print item.value['name'] + '\t' + item.uuid

    # write to cache
    vdjpy.write_json(projects, projects_cache)
