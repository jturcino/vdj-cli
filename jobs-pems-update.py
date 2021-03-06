#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Update job permissions for a user. Permission options are READ, WRITE, EXECUTE, READ_WRITE, READ_EXECUTE, WRITE_EXECUTE, ALL, or NONE.')
    parser.add_argument('-j', '--jobID', dest = 'jobID', nargs = '?', help = 'job ID')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?', help = 'username to be updated')
    parser.add_argument('-p', '--permissions', dest = 'permissions', nargs = '?', help = 'permissions to grant to user')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()
    
    kwargs = {}

    # -j
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('jobID')
    kwargs['jobId'] = args.jobID

    # -u
    if args.username is None:
        args.username = vdjpy.prompt_user('username')

    # -p
    if args.permissions is None:
        print 'Valid permission options are as follows: \n\tREAD \n\tWRITE \n\tEXECUTE \n\tREAD_WRITE \n\tREAD_EXECUTE \n\tWRITE_EXECUTE \n\tALL \n\tNONE'
        args.permissions = vdjpy.prompt_user('permission to set')

    # build body
    kwargs['body'] = "{\n\t\"username\":\"" + args.username + "\",\n\t\"permission\": \"" + args.permissions + "\"\n}"

    # update permissions 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_update = my_agave.jobs.updatePermissions(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(pems_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Permissions for', args.username, 'now set to \n\tread:', pems_update['permission']['read'], '\n\twrite:', pems_update['permission']['write']
