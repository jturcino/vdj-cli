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

    # make agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('current file name')

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()

    # -d
    if args.new_name is None:
        args.new_name = vdjpy.prompt_user('new name')

    # get metadata for file
    project_files = vdjpy.get_project_files(uuid, {}, my_agave)
    file_metadata = None
    for item in project_files:
        if item['value']['name'] == args.file_name:
            file_metadata = item
    
    # if file metadata not found, exit
    if file_metadata is None:
        print 'The file', args.file_name, 'does not exist in project', args.project + '. \nHere are the files currently in the project:'
        for item in project_files:
            print item['value']['name']
        sys.exit()

    # change value.name to desired name if file found
    file_metadata['value']['name'] = unicode(args.new_name)

    # rename in agave and via metadata update
    agave_rename = my_agave.files.manage(systemId = 'data.vdjserver.org',
					 filePath = '/projects/' + uuid + '/files/' + args.file_name, 
					 body = {'action': 'rename', 'path': args.new_name})
    metadata_update = my_agave.meta.updateMetadata(uuid = file_metadata['uuid'], 
						   body = json.dumps(file_metadata))

    # if -v
    if args.verbose:
         print json.dumps(agave_rename, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
         print json.dumps(metadata_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now renaming file', args.file_name, 'in project', args.project, 'to', str(metadata_update['value']['name'])
