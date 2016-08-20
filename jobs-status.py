#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Return status of a job.')
    parser.add_argument('-j', '--jobID', dest = 'jobID', nargs = '?', help = 'job ID')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()
    
    kwargs = {}

    # -j
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('jobID')
    kwargs['jobId'] = args.jobID

    # get status 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    status = my_agave.jobs.getStatus(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(status, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'The status of job',  args.jobID, 'is', status['status']
