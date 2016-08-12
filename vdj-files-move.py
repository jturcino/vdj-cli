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
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
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

    # -d
    if args.destination_project is None:
        args.destination_project = vdjpy.prompt_user('destination project')
    destination_uuid = vdjpy.get_uuid(args.destination_project, my_agave)
    if destination_uuid is None:
        sys.exit()

    # SET UP FILETYPE AND GET FILE NAME IN ARGS.FILE_NAME
    # -f (default file type)
    if args.file_name is not '' or args.jobfile_name is '':
        if args.file_name is None:
            args.file_name = vdjpy.prompt_user('file name')
        filetype = 'projectFile'
    # -j (only used if given)
    else:
        if args.jobfile_name is None:
            args.jobfile_name = vdjpy.prompt_user('jobfile name')
        filetype = 'projectJobFile'
        args.file_name = args.jobfile_name

    # get metadata for file; exit if file not found
    project_files = vdjpy.get_project_files(current_uuid, filetype, {}, my_agave)
    file_metadata = vdjpy.get_file_metadata(project_files, args.file_name)
    if file_metadata is None:
        sys.exit()

    # if jobfile, get extra path; then build paths
    extra_path = ''
    if filetype == 'projectJobFile':
	extra_path += str(file_metadata['value']['relativeArchivePath']) + '/'
    current_path = vdjpy.build_vdj_path(current_uuid, args.file_name, filetype, extra_path)
    destination_path = vdjpy.build_vdj_path(destination_uuid, args.file_name, 'projectFile', '')

    # move in agave (cannot move to jobfile destination)
    agave_move = my_agave.files.manage(systemId = 'data.vdjserver.org',
				       filePath = current_path, 
				       body = {'action': 'move', 
					       'path': destination_path})

    # update filepath, project uuid, and remove unnecessary metadata if jobfile
    file_metadata['_links']['file']['href'] = unicode('https://vdj-agave-api.tacc.utexas.edu/files/v2/media/system/data.vdjserver.org/' + destination_path)
    file_metadata['value']['projectUuid'] = unicode(destination_uuid)
    if filetype == 'projectJobFile':
	file_metadata['name'] = 'projectFile'
        del file_metadata['value']['relativeArchivePath']
        del file_metadata['value']['jobName']
        del file_metadata['value']['jobUuid']

    # update metadata
    metadata_update = my_agave.meta.updateMetadata(uuid = file_metadata['uuid'], 
						   body = json.dumps(file_metadata))

    # if -v
    if args.verbose:
        print json.dumps(agave_move, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        print json.dumps(metadata_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now moving', str(agave_move['name']), 'from project', args.current_project, 'to project', args.destination_project 
