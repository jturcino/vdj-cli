#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Update a user\'s permissions for a file or directory on a remote system. System defaults to data.vdjserver.org. Permissions options are READ, WRITE, EXECUTE, READ_WRITE, READ_EXECUTE, WRITE_EXECUTE, ALL, or NONE.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?', help = 'username to update permissions')
    parser.add_argument('-a', '--access', dest = 'access', nargs = '?', help = 'permissions to grant to user')
    parser.add_argument('-r', '--recursive', dest = 'recursive', action = 'store_true', help = 'applies recursive permissions')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # -r
    recursive = 'false'
    if args.recursive:
        recursive = 'true'

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -u
    if args.username is None:
        args.username = vdjpy.prompt_user('username to update')
    
    if args.access is None:
        print 'Valid permission options are as follows: \n\tREAD \n\tWRITE \n\tEXECUTE \n\tREAD_WRITE \n\tREAD_EXECUTE \n\tWRITE_EXECUTE \n\tALL \n\tNONE'
        args.access = vdjpy.prompt_user('permission to set')

    # build body
    kwargs['body'] = "{\n\t\"username\":\"" + args.username + "\",\n\t\"permission\": \"" + args.access + "\",\n\t\"recursive\":" + recursive + "\n}"

    # update permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_update = my_agave.files.updatePermissions(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(pems_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Permissions for', args.username, 'now set to \n\texecute:', pems_update[0]['permission']['execute'], '\n\tread:', pems_update[0]['permission']['read'], '\n\twrite:', pems_update[0]['permission']['write'], '\n\trecursive:', args.recursive
