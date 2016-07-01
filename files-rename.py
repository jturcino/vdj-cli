#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--system', dest = 'system', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-n', '--new_name', dest = 'new_name', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.system is None:
        args.system = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.system

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -d
    if args.new_name is None:
        args.new_name = vdjpy.prompt_user('new name')
    kwargs['body']  = {'action': 'rename', 'path': args.new_name}

    # rename
    rename = my_agave.files.manage(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(rename, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now renaming file at', args.path, 'to', str(rename['name'])