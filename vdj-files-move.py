#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--current_project', dest = 'current_project', default = None, nargs = '?')
    parser.add_argument('-d', '--destination_project', dest = 'destination_project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

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

    # get metadata for file
    project_files = vdjpy.get_project_files(current_uuid, {}, my_agave)
    file_metadata = None
    for item in project_files:
        if item['value']['name'] == args.file_name:
            file_metadata = item

    # if file metadata not found, exit
    if file_metadata is None:
        print 'The file', args.file_name, 'does not exist in project', args.current_project + '. \nHere are the files currently in the project:'
        for item in project_files:
            print item['value']['name']
        sys.exit()

    # change project uuid to destination uuid
    file_metadata['_links']['file']['href'] = unicode('https://vdj-agave-api.tacc.utexas.edu/files/v2/media/system/data.vdjserver.org//projects/' + destination_uuid + '/files/' + args.file_name)
    file_metadata['value']['projectUuid'] = unicode(destination_uuid)

    # move in agave and metadata update
    agave_move = my_agave.files.manageOnDefaultSystem(sourcefilePath = '/projects/' + current_uuid + '/files/' + args.file_name, 
						      body = {'action': 'move', 'path': '/projects/' + destination_uuid + '/files/' + args.file_name})
    metadata_update = my_agave.meta.updateMetadata(uuid = file_metadata['uuid'], body = json.dumps(file_metadata))

    # if -v
    if args.verbose:
        print json.dumps(agave_move, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        print json.dumps(metadata_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now moving', str(agave_move['name']), 'from project', args.current_project, 'to project', args.destination_project 
