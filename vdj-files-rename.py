#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
    parser.add_argument('-n', '--new_name', dest = 'new_name', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()

    # -f (default)
    if args.file_name is not '' or args.jobfile_name is '':
	if args.file_name is None:
            args.file_name = vdjpy.prompt_user('current file name')
	filetype = 'projectFile'
    # -j (only used if specified)
    else:
	if args.jobfile_name is None:
	    args.jobfile_name = vdjpy.prompt_user('current jobfile name')
	filetype = 'projectJobFile'
	# consolidate file name to args.file_name
	args.file_name = args.jobfile_name

    # -d
    if args.new_name is None:
        args.new_name = vdjpy.prompt_user('new name')

    # get metadata for file; exit if not found
    project_files = vdjpy.get_project_files(uuid, filetype, {}, my_agave)
    file_metadata = vdjpy.get_file_metadata(project_files, args.file_name)
    if file_metadata is None:
        sys.exit()

    # if jobfile, get extra path
    extra_path = ''
    if filetype == 'projectJobFile':
        extra_path += str(file_metadata['value']['relativeArchivePath']) + '/'

    # change value.name to desired name
    file_metadata['value']['name'] = unicode(args.new_name)

    # rename in agave and via metadata update
    agave_rename = my_agave.files.manage(systemId = 'data.vdjserver.org',
					 filePath = vdjpy.build_vdj_path(uuid, args.file_name, filetype, extra_path), 
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
