#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--description_file', dest = 'description_file', default = None)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing app description')
    
    # open -f and use as body
    if os.path.isfile(os.path.expanduser(args.description_file)) is True:
        with open(os.path.expanduser(args.description_file), 'r') as description_file:
            kwargs['body'] = json.dumps(json.load(description_file))
    else:
        sys.exit('Not a valid file path.')

    # publish app
    publish = my_agave.apps.add(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(publish, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully added app', publish['id']
