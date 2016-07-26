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
    parser.add_argument('-n', '--clone_name', dest = 'clone_name', default = '', nargs = '?')
    parser.add_argument('-s', '--storage_system', dest = 'storage_system', default = None, nargs = '?')
    parser.add_argument('-e', '--execution_system', dest = 'execution_system', default = '', nargs = '?')
    parser.add_argument('-x', '--version', dest = 'version', default = '', nargs = '?')
    parser.add_argument('-d', '--deployment_path', dest = 'deployment_path', default = None, nargs = '?')
    parser.add_argument('-f', '--description_file', dest = 'description_file', default = '', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -a
    if args.appID is None:
        args.appID = vdjpy.prompt_user('ID of app to be cloned')
    kwargs['appId'] = args.appID

    # -f used if given
    if args.description_file is not '':
        if args.description_file is None:
            args.description_file = vdjpy.prompt_user('file name')
        body_contents = vdjpy.read_json(args.description_file)
        if body_contents is None:
            sys.exit()
        kwargs['body'] = body_contents #DOES IT NEED TO BE STRING???

    # -n, -s, -e, -x, and -d used if no -f
    else:
        # if -n, -e, or -x not given, load app data (exit if app does not exist)
        if args.clone_name or args.execution_system or args.version is '':
            apps = my_agave.apps.list()
            app_info = None
            for app in apps:
                if app['id'] == args.appID:
                    app_info = app
            if app_info is None:
                sys.exit('Could not find given app in your apps')
        # -n
        if args.clone_name is '':
            vdjapi_contents = vdjpy.read_json('~/.vdjapi')
            try:
                username = vdjapi_contents.get('username')
            except:
                sys.exit('Unable to get username from ~/.vdjapi')
            args.clone_name = app_info['name'] + '-' + username
        elif args.clone_name is None:
            args.clone_name = vdjpy.prompt_user('name of cloned app')

        # -e
        if args.execution_system is '':
            args.execution_system = app_info['executionSystem']
        elif args.execution_system is None:
            args.execution_system = vdjpy.prompt_user('execution system')

        # -x
        if args.version is '':
            args.version = app_info['version']
        elif args.version is None:
            args.version = vdjpy.prompt_user('version of cloned app')

        # -s
        if args.storage_system is None:
            args.storage_system = vdjpy.prompt_user('storage system')

        # -d
        if args.deployment_path is None:
            args.deployment_path = vdjpy.prompt_user('deployment path')


        # build body
        kwargs['body'] = {'action': 'clone',
			  'name': args.clone_name,
			  'storageSystem': args.storage_system,
			  'executionSystem': args.execution_system,
			  'version': args.version,
			  'deploymentPath': args.deployment_path}

    # clone app
    clone = my_agave.apps.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(clone, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully cloned app', clone['id']
