#!/usr/bin/env python

import vdjpy
import argparse
import json

def sortbydatetime(jsonlist, query):
    """Takes a list of json dictionaries with a query by which to sort the list"""
    jsonlist = sorted(jsonlist, key = itemgetter(query))
    return jsonlist

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-s', '--sort', dest = 'sort', default = '', nargs = '?')
    args = parser.parse_args()

    # cache
    projects_cache = './.vdjprojects'

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)

    # make object
    projects = vdjpy.get_vdj_projects(args.accesstoken, args.limit, args.offset)
    
    # if -t
    if args.sort is not '':
        projects = vdjpy.sortbyquery(projects, args.sort)

    # if -v
    if args.verbose is True:
        print json.dumps(projects, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
       for item in projects:
           print item.value['name'] + ' ' + item.uuid

    # write to cache
    vdjpy.write_json(projects, projects_cache)
