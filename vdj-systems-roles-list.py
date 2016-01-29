#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', required = True)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # get token
    access_token = vdjpy.read_cache('access_token')
    if access_token is None:
        access_token = vdjpy.prompt_user('access_token')

    # get systems roles
    my_agave = vdjpy.make_vdj_agave(access_token)
    roles_list = my_agave.systems.listRoles(systemId = args.systemID)

    # if -v
    if args.verbose is True:
        print json.dumps(roles_list, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for system in roles_list:
            print str(system['username']), str(system['role'])
