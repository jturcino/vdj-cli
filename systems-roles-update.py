#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Updates a user\'s role on a system. Possible roles for a user are USER, PUBLISHER, ADMIN, and OWNER.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?', help = 'system ID')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?', help = 'username to be updated')
    parser.add_argument('-r', '--role', dest = 'role', nargs = '?', help = 'role to give user')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
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
    if args.role != "USER" or "PUBLISHER" or "ADMIN" or "OWNER" or None:
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
