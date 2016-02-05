#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        args.accesstoken = vdjpy.read_cache('access_token')
        if args.accesstoken is None:
            args.accesstoken = vdjpy.prompt_user('access_token')

    # check systemID
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    roles_list = my_agave.systems.listRoles(systemId = args.systemID)

    # if -v
    if args.verbose is True:
        print json.dumps(roles_list, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for system in roles_list:
            print str(system['username']), str(system['role'])
