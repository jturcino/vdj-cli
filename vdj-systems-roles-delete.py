#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = None, nargs = '?')
    parser.add_argument('-u', '--username', dest = 'username', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
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
    
    print 'User', args.username, 'now deleted from', args.systemID
