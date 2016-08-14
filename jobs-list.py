#!/usr/bin/env python

import json
import argparse
import vdjpy
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jobID', dest = 'jobID', default = '', nargs = '?') 
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # IF JOBID, GET JOB INFO, PRINT, AND EXIT
    if args.jobID is not '':
	if args.jobID is None:
	    args.jobID = vdjpy.prompt_user('job ID')
	resp = my_agave.jobs.get(jobId = args.jobID)
        print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
	sys.exit()

    # IF NO APPID, LIST JOBS
    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # list jobs
    jobs = my_agave.jobs.list(**kwargs)
    
    # -v
    if args.verbose:
        print json.dumps(jobs, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in jobs:
            print item['name'], '\t\t', item['id']
