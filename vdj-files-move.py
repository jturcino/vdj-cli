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
	# consolidate file name to args.file_name
	args.jobfile_name = args.file_name

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

    # get metadata for file; exit if file not found
    project_files = vdjpy.get_project_files(current_uuid, filetype, {}, my_agave)
    file_metadata = vdjpy.get_file_metadata(project_files, args.file_name)
    if file_metadata is None:
        sys.exit()

    # get extra path if is jobfile
    extra_path = ''
    if filetype == 'projectJobFile':
	extra_path += str(file_metadata['value']['relativeArchivePath']) + '/'

    # change project uuid to destination uuid
    file_metadata['_links']['file']['href'] = unicode('https://vdj-agave-api.tacc.utexas.edu/files/v2/media/system/data.vdjserver.org/' + vdjpy.build_vdj_path(destination_uuid, args.file_name, filetype, extra_path))
    file_metadata['value']['projectUuid'] = unicode(destination_uuid)

    # move in agave and metadata update
    agave_move = my_agave.files.manage(systemId = 'data.vdjserver.org',
				       filePath = vdjpy.build_vdj_path(current_uuid, args.file_name, filetype, extra_path), 
				       body = {'action': 'move', 
					       'path': vdjpy.build_vdj_path(destination_uuid, args.file_name, 'projectFile', '')}) # JOBFILE DEST NOT AVAILABLE
    metadata_update = my_agave.meta.updateMetadata(uuid = file_metadata['uuid'], 
						   body = json.dumps(file_metadata))

    # if -v
    if args.verbose:
        print json.dumps(agave_move, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        print json.dumps(metadata_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now moving', str(agave_move['name']), 'from project', args.current_project, 'to project', args.destination_project 
