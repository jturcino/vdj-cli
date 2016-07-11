#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-n', '--new_name', dest = 'new_name', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('current file name')

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()
    kwargs['sourcefilePath'] = '/projects/' + uuid + '/files/' + args.file_name

    # -d
    if args.new_name is None:
        args.new_name = vdjpy.prompt_user('new name')
    kwargs['body']  = {'action': 'rename', 'path': args.new_name}

    # rename
    rename = my_agave.files.manageOnDefaultSystem(**kwargs)

    # INSERT WORKING METADATA UPDATE HERE

    # if -v
    if args.verbose:
         print json.dumps(rename, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now renaming file', args.file_name, 'in project', args.project, 'to', str(rename['name'])
