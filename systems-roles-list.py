#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?')
    parser.add_argument('-u', '--username', dest = 'username', default = '', nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # check systemID
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # check username
    if args.username is not '':
        if args.username is None:
            args.username = vdjpy.prompt_user('username')
        kwargs['username'] = args.username

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # if -u
    if args.username is not '':
        roles_list = my_agave.systems.getRoleForUser(**kwargs)

    # if no -u
    else:
        roles_list = my_agave.systems.listRoles(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(roles_list, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        if type(roles_list) is list:
            for system in roles_list:
                print str(system['username']), str(system['role'])
        else:
            print str(roles_list['username']),  str(roles_list['role'])
