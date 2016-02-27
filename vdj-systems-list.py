#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    parser.add_argument('-S', '--storageonly', dest = 'storageonly', action = 'store_true')
    parser.add_argument('-E', '--executiononly', dest = 'executiononly', action = 'store_true')
    parser.add_argument('-D', '--default', dest = 'default', action = 'store_true')
    parser.add_argument('-Q', '--private', dest = 'private', action = 'store_true')
    parser.add_argument('-P', '--public', dest = 'public', action = 'store_true')
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

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    systems = my_agave.systems.list(**kwargs)

    # verbose/standard output
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))
    else:
        for system in systems:
            print str(system['id'])
