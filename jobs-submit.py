#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Submit a job.')
    parser.add_argument('-f', '--description_file', dest = 'description_file', nargs = '?', help = 'file containing JSON job description')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing app description')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.description_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid app description.')
    kwargs['body'] = json.dumps(body_contents)

    # submit job
    submit = my_agave.jobs.submit(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(submit, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'job', submit['name'], 'submitted \nid:', submit['id'], '\nstatus:', submit['status']
