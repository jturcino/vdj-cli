#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys
import urllib

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appID', dest = 'appID', nargs = '?')
    parser.add_argument('-n', '--clone_name', dest = 'clone_name', default = '', nargs = '?')
    parser.add_argument('-s', '--deployment_system', dest = 'deployment_system', nargs = '?')
    parser.add_argument('-e', '--execution_system', dest = 'execution_system', nargs = '?')
    parser.add_argument('-x', '--version', dest = 'version', default = '', nargs = '?')
    parser.add_argument('-d', '--deployment_path', dest = 'deployment_path', nargs = '?')
    parser.add_argument('-f', '--description_file', dest = 'description_file', default = '', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
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
        kwargs['body'] = json.dumps(body_contents)

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
                sys.exit('Could not find app to be cloned')
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
        if args.execution_system is None:
            args.execution_system = vdjpy.prompt_user('execution system')

        # -x
        if args.version is '':
            args.version = app_info['version']
        elif args.version is None:
            args.version = vdjpy.prompt_user('version of cloned app')

        # -s
        if args.deployment_system is None:
            args.deployment_system = vdjpy.prompt_user('deployment system')

        # -d
        if args.deployment_path is None:
            args.deployment_path = vdjpy.prompt_user('deployment path')

        # build body
        kwargs['body'] = json.dumps({'action': 'clone',
			  'name': str(args.clone_name),
			  'deploymentSystem': str(args.deployment_system),
			  'executionSystem': str(args.execution_system),
			  'version': str(args.version),
			  'deploymentPath': str(args.deployment_path)})

    # clone app
    clone = my_agave.apps.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(clone, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully cloned app', clone['id']
