#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?')
    parser.add_argument('-r', '--role', dest = 'role', nargs = '?')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # check systemID
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID
    
    # check username
    if args.username is None:
        args.username = vdjpy.prompt_user('username to add')
    kwargs['username'] = args.username

    # check role
    if args.role is not None:
         args.role = args.role.upper()
    if args.role is not "USER" or not "PUBLISHER" or not "ADMIN" or not "OWNER" or None:
        print 'Possible roles for', args.username, 'are USER, PUBLISHER, ADMIN, and OWNER. \nPlease enter the selected role:',
        args.role = raw_input('')
    kwargs['body'] = {'username':args.username, 'role':args.role.upper()}

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    role_update = my_agave.systems.updateRoleForUser(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(role_update, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Sucessfully updated role for', role_update[0]['username'], 'to', role_update[0]['role']
