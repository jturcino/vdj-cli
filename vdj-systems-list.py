#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    parser.add_argument('-s', '--storageonly', dest = 'storageonly', action = 'store_true')
    parser.add_argument('-e', '--executiononly', dest = 'executiononly', action = 'store_true')
    parser.add_argument('-d', '--default', dest = 'default', action = 'store_true')
    parser.add_argument('-q', '--private', dest = 'private', action = 'store_true')
    parser.add_argument('-p', '--public', dest = 'public', action = 'store_true')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # storage/execution
    if args.storageonly and not args.executiononly:
        kwargs['type'] = 'STORAGE'
    elif args.executiononly and not args.storageonly:
        kwargs['type'] = 'EXECUTION'
    
    # default
    if args.default:
        kwargs['default'] = True

    # private/public
    if args.public and not args.private:
        kwargs['public'] = True
    elif args.private and not args.public:
        kwargs['public'] = False

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    systems = my_agave.systems.list(**kwargs)

    # verbose/standard output
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))
    else:
        for system in systems:
            print str(system['id'])
