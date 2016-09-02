#!/usr/bin/env python

import vdjpy
import argparse
import json

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'List the user\'s projects on data.vdjserver.org.Results can be sorted alphabetically.')
    parser.add_argument('-u', '--show_uuids', dest = 'show_uuids', action = 'store_true', help = 'list project uuids')
    parser.add_argument('-s', '--alphabetical_sort', dest = 'alphabetical_sort', action = 'store_true', help = 'list alphabetically')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # cache
    projects_cache = '~/.vdjprojects'

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # get projects
    projects = vdjpy.get_vdj_projects(my_agave, kwargs)
    
    # if -s
    if args.alphabetical_sort:
	projects.sort(key = lambda e: e['value']['name'])

    # if -v
    if args.verbose is True:
        print json.dumps(projects, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
       for item in projects:
           # if args.show_uuids, print uuid with name
           if args.show_uuids:
               print item.value['name'] + '\t' + item.uuid
           else:
               print item.value['name']

    # write to cache
    vdjpy.write_json(projects, projects_cache)
