#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appID', dest = 'appID', default = None, nargs = '?')
    parser.add_argument('-n', '--clone_name', dest = 'clone_name', default = None, nargs = '?')
    parser.add_argument('-s', '--storage_system', dest = 'storage_system', default = None, nargs = '?')
    parser.add_argument('-e', '--execution_system', dest = 'execution_system', default = None, nargs = '?')
    parser.add_argument('-x', '--version', dest = 'version', default = None, nargs = '?')
    parser.add_argument('-d', '--deployment_path', dest = 'deployment_path', default = None, nargs = '?')
#    parser.add_argument('-f', '--description_file', dest = 'description_file', default = None)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

   # -a
   if args.appID is None:
        args.appID = vdjpy.prompt_user('ID of app to be cloned)
   kwargs['appId'] = args.appID

#############################################
# if -f, use
# else, use inputs
    # if -n, -s,  -e, -x, or -d not given
        # load app info
        # use app info to populate args
    # build body
############################################

    # -f
    if args.description_file is None:
        args.description_file = vdjpy.prompt_user('path to file containing app description')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.description_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid app description.')
    kwargs['body'] = json.dumps(body_contents)

    # clone app
    clone = my_agave.apps.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(clone, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully added app', clone['id']
