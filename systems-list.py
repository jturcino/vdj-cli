#!/usr/bin/env python

import json
import argparse
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = '', nargs = '?')
    parser.add_argument('-x', '--storageonly', dest = 'storageonly', action = 'store_true')
    parser.add_argument('-e', '--executiononly', dest = 'executiononly', action = 'store_true')
    parser.add_argument('-d', '--default', dest = 'default', action = 'store_true')
    parser.add_argument('-q', '--private', dest = 'private', action = 'store_true')
    parser.add_argument('-p', '--public', dest = 'public', action = 'store_true')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # IF SYSTEMID, GET SYSTEM INFO, PRINT, AND EXIT
    if args.systemID is not '':
	if args.systemID is None:
	    args.systemID = vdjpy.prompt_user('system ID')
	resp = my_agave.systems.get(systemId = args.systemID)
	print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
	sys.exit()

    # IF NO SYSTEMID, LIST SYSTEMS
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
