#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Register a new system or update a current system. If the ID of an existing system is given, the system will be updated; otherwise, a new system will be created.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = '', nargs = '?', help = 'system ID')
    parser.add_argument('-f', '--description_file', dest = 'description_file', nargs = '?', help = 'file containing JSON system description')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing system description')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.description_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid system description.')
    kwargs['body'] = json.dumps(body_contents)

    # if -s given, update system
    if args.systemID is not '':
        if args.systemID is None:
	    args.systemID = vdjpy.prompt_user('system ID')
	kwargs['systemId'] = args.systemID
	resp = my_agave.systems.update(**kwargs)

    # else, add system
    else:
	resp = my_agave.systems.add(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    elif args.systemID is not '':
        print 'Successfully updated system', resp['id']
    else:
	print 'Successfully added system', resp['id']
