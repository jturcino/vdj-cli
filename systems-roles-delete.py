#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Remove roles for a user on a system.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?', help = 'system ID')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?', help = 'user to be removed')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # system
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # username
    if args.username is None:
        args.username = vdjpy.prompt_user('username to delete from system')
    kwargs['username'] = args.username

    # get systems
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    role_delete = my_agave.systems.deleteRoleForUser(**kwargs)
    
    if role_delete is None:
        print 'Succesfully removed permissions for app', args.appID
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(role_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
