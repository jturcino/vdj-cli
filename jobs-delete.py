#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Delete an existing job.')
    parser.add_argument('-j', '--jobID', dest = 'jobID', nargs = '?', help = 'job ID')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()
    
    kwargs = {}

    # -j
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('jobID')
    kwargs['jobId'] = args.jobID

    # get status 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    job_delete = my_agave.jobs.delete(**kwargs)

    # deliver message
    if job_delete is None:
        print 'Successfully deleted job', args.jobID
    else:
        print 'Deletion failed. Message returned from request is:\n' + json.dumps(job_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
