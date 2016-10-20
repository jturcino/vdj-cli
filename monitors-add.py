#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Register a new monitor for a system. There may be only one monitor per system.')
    parser.add_argument('-f', '--description_file', dest = 'description_file', nargs = '?', help = 'file containing JSON monitor description')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing monitor description')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.description_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid monitor description.')
    kwargs['body'] = json.dumps(body_contents)

    # add monitor
    resp = my_agave.monitors.add(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
	print 'Successfully added monitor', resp['id']
