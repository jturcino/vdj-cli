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
    parser.add_argument('-u', '--username', dest = 'username', default = '', nargs = '?')
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

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # if -u
    if args.username:
        roles_list = my_agave.systems.getRoleForUser(**kwargs)
        print roles_list
    # if no -u
    else:
        roles_list = my_agave.systems.listRoles(**kwargs)
    for system in roles_list:
        print str(system['username']), str(system['role'])

    # if -v
#    if args.verbose is True:
#    print json.dumps(roles_list, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
#    else:
#        for system in roles_list:
#            print str(system['username']), str(system['role'])
