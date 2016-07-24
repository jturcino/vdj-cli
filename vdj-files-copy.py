#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--current_project', dest = 'current_project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
    parser.add_argument('-d', '--destination_project', dest = 'destination_project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -p
    if args.current_project is None:
        args.current_project = vdjpy.prompt_user('current project')
    current_uuid = vdjpy.get_uuid(args.current_project, my_agave)
    if current_uuid is None:
        sys.exit()

    # -f
    if args.file_name is None or args.jobfile_name is '':
        args.file_name = vdjpy.prompt_user('file name')

    # -j (only if no -f)
    if args.jobfile_name is None and args.file_name is '':
        args.jobfile_name = vdjpy.prompt_user('jobfile name')

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

    # copy file with agave
    agave_copy = my_agave.files.manage(systemId = 'data.vdjserver.org', 
				       filePath = vdjpy.build_vdj_path(current_uuid, args.file_name, args.jobfile_name),
				       body = {'action': 'copy', 'path': vdjpy.build_vdj_path(destination_uuid, args.file_name, args.jobfile_name)})

    # create new metadata and add
    file_metadata['value']['projectUuid'] = destination_uuid
    new_metadata = {
        'associationIds': [agave_copy['uuid']],
        'name': 'projectFile',
        'schemaId': None,
        'value': file_metadata['value']
    }
    metadata_create = my_agave.meta.addMetadata(body = json.dumps(new_metadata))


    # if -v
    if args.verbose:
         print json.dumps(agave_copy, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
         print json.dumps(metadata_create, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now copying', str(agave_copy['name']), 'from', args.current_project, 'to', args.destination_project
