#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # list jobs
    my_agave = vdjpy.make_vdj_agave(None)
    jobs = my_agave.jobs.list()
    
    # -v
    if args.verbose:
        print json.dumps(jobs, default = json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in jobs:
            print item['name'], '\n\tid:', item['id'], '\n\tstatus:', item['status']
