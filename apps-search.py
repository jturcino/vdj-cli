#!/usr/bin/env python

import argparse
import json
import vdjpy
import ast

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Search for apps based on attributes. Values must be in dictionary form such as {"executionSystem.like": "*stampede*"} or {"id.like": "vdj_pipe*"}.')
    parser.add_argument('-q', '--query', dest = 'query', nargs = '?', help = 'search query in dictionary form')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -q
    if args.query is None:
        print 'Queries must be in dictionary form. Some example queries are: \n\t{"executionSystem.like": "*stampede*"} \n\t{"id.like": "vdj_pipe*"}'
        args.query = vdjpy.prompt_user('search query')
    try:
        kwargs['search'] = ast.literal_eval(args.query)
    except:
        sys.exit('Given query is not a valid dictionary')

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # search systems
    apps = my_agave.apps.list(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(apps, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for app in apps:
            print str(app['id'])
