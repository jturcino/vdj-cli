#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--systemID', dest = 'systemID', default = None)
    parser.add_argument('-f', '--description_file', dest = 'description_file', default = None)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -a
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing system description')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.description_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid system description.')
    kwargs['body'] = json.dumps(body_contents)

    # update system
    update = my_agave.systems.update(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully updated system', args.systemID
