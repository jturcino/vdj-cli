#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jobID', dest = 'jobID', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()
    
    kwargs = {}

    # -j
    if args.jobID is None:
        args.jobID = vdjpy.prompt_user('jobID')
    kwargs['jobId'] = args.jobID

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get history
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems = my_agave.jobs.listPermissions(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(pems, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
       for item in pems:
            user_pems = ''
            if item['permission']['read']:
                user_pems += 'r'
            if item['permission']['write']:
                user_pems += 'w'
            print item['username'], user_pems 
