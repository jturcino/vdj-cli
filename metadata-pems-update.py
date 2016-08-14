#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uuid', dest = 'uuid', nargs = '?')
    parser.add_argument('-n', '--username', dest = 'username', nargs = '?')
    parser.add_argument('-p', '--permissions', dest = 'permissions', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # -u
    if args.uuid is None:
        args.uuid = vdjpy.prompt_user('uuid of item')
    kwargs['uuid'] = args.uuid

    # -n
    if args.username is None:
        args.username = vdjpy.prompt_user('username')

    # -p
    if args.permissions is None:
        print 'Valid permission options are as follows: \n\tREAD \n\tWRITE \n\tEXECUTE \n\tREAD_WRITE \n\tREAD_EXECUTE \n\tWRITE_EXECUTE \n\tALL \n\tNONE'
        args.permissions = vdjpy.prompt_user('permissions')

    # build body
    kwargs['body'] = "{\n\t\"username\":\"" + args.username + "\",\n\t\"permission\": \"" + args.permissions + "\"\n}"

    # list permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_update = my_agave.meta.updateMetadataPermissions(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(pems_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Permissions for', args.username, 'now set to \n\tread:', pems_update['permission']['read'], '\n\twrite', pems_update['permission']['write']
