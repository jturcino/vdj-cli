#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Resubmit a job. Original inputs and parameters are used and a new jobID is assigned.')
    parser.add_argument('-j', '--jobID', dest = 'jobID', default = None, nargs = '?', help = 'job ID')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['body'] = {'action': 'resubmit'}

    # -j
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('job ID')
    kwargs['jobId'] = args.jobID

    # resubmit job
    resubmit = my_agave.jobs.manage(**kwargs)


    # if -v
    if args.verbose:
        print json.dumps(resubmit, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now resubmitting job', resubmit['name'], '\nid:', resubmit['id'], '\nstatus:', resubmit['status']
