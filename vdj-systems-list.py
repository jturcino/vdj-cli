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
    parser.add_argument('-D', '--defaultonly', dest = 'defaultonly', action = 'store_true')
    parser.add_argument('-Q', '--privateonly', dest = 'privateonly', action = 'store_true')
    parser.add_argument('-P', '--publiconly', dest = 'publiconly', action = 'store_true')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        args.accesstoken = vdjpy.read_cache('access_token')
        if args.accesstoken is None:
            args.accesstoken = vdjpy.prompt_user('access_token')

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    if args.storageonly:
        systems = my_agave.systems.list(default = args.defaultonly, privateOnly = args.privateonly, publicOnly = args.publiconly, type = 'STORAGE')
    elif args.executiononly:
        systems = my_agave.systems.list(default = args.defaultonly, privateOnly = args.privateonly, publicOnly = args.publiconly, type = 'EXECUTION') 
    else:
        systems = my_agave.systems.list(default = args.defaultonly, privateOnly = args.privateonly, publicOnly = args.publiconly)

    # restrict output (check for storage, execution, default, and/or private only flags)
#    if args.storageonly is True:
#        systems = vdjpy.restrict_systems(systems, 'STORAGE')
#    elif args.executiononly is True:
#        systems = vdjpy.restrict_systems(systems, 'EXECUTION')

    # if -v
    if args.verbose is True:
        print json.dumps(systems, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for system in systems:
            print str(system['id'])
