#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--current_project', dest = 'current_project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-d', '--destination_project', dest = 'destination_project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['systemId'] = 'data.vdjserver.org'

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('file name')

    # -p
    if args.current_project is None:
        args.current_project = vdjpy.prompt_user('current project')
    current_uuid = vdjpy.get_uuid(args.current_project, my_agave)
    if current_uuid is None:
        sys.exit()

    # -d
    if args.destination_project is None:
        args.destination_project = vdjpy.prompt_user('destination project')
    destination_uuid = vdjpy.get_uuid(args.destination_project, my_agave)
    if destination_uuid is None:
        sys.exit()

    # current path
    kwargs['filePath'] = '/projects/' + current_uuid + '/files/' + args.file_name
    print kwargs['filePath']

    # build body
    destination_path = '/projects/' + destination_uuid + '/files/'
    kwargs['body'] = {'action': 'copy', 'path': destination_path}
    print kwargs['body']

    # copy file
    copy = my_agave.files.manage(**kwargs)

    # update metadata
    file_uuid = str(copy['uuid'])
    resp = vdjpy.update_metadata(destination_uuid, args.file_name, file_uuid, '')

    # if -v
    if args.verbose:
         print json.dumps(copy, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
         print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now copying', str(copy['name']), 'from', args.current_project, 'to', args.destination_project
