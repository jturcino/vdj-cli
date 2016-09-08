#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Delete all permissions on an job.')
    parser.add_argument('-a', '--jobID', dest = 'jobID', nargs = '?', help = 'job ID')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # -p
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('jobID')
    kwargs['jobId'] = args.jobID

    # delete permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_delete = my_agave.jobs.deletePermissions(**kwargs)

    if pems_delete is None:
        print 'Succesfully removed permissions for job', args.jobID
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(pems_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
