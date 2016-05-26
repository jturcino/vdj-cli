#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--current_project', dest = 'current_project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-d', '--destination_project', dest = 'destination_project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('file name')

    # -p
    if args.current_project is None:
        args.current_project = vdjpy.prompt_user('file\'s current project')
    current_uuid = vdjpy.get_uuid(args.current_project, args.accesstoken)

    # -d
    if args.destination_project is None:
        args.destination_project = vdjpy.prompt_user('project to copy the file')
    destination_uuid = vdjpy.get_uuid(args.destination_project, args.accesstoken)

    current_path = '/projects/' + current_uuid + '/files/' + args.file_name
    destination_path = '/projects/' + destination_uuid + '/files'
    data_change = "{\"action\":\"copy\",\"path\": \"" + destination_path + "\"}"

    # copy file
    copy = vdjpy.manage_files(args.accesstoken, None, current_path, data_change)

    # update metadata
    file_uuid = str(copy['uuid'])
    extras = ''
    resp = vdjpy.update_metadata(destination_uuid, args.file_name, file_uuid, extras)

    # if -v
    if args.verbose:
         print json.dumps(copy, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
         print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now copying', str(copy['name']), 'from', args.current_project, 'to', args.destination_project
