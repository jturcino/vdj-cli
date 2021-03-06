#!/usr/bin/env python

import vdjpy
import argparse
import sys
import json


if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Delete a projectfile or jobfile on data.vdjserver.org. This command updates metadata, and the deleted file will no longer be visible on vdjserver.org.')
    parser.add_argument('-p', '--project', dest = 'project', nargs = '?', help = 'name of file\'s project')
    parser.add_argument('-f', '--file_to_delete', dest = 'file_to_delete', default = '', nargs = '?', help = 'name of projectfile')
    parser.add_argument('-j', '--jobfile_to_delete', dest = 'jobfile_to_delete', default = '', nargs = '?', help = 'name of jobfile')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit()
    project_uuid = str(project_uuid)

    # SET UP FILETYPE AND GET FILE NAME IN ARGS.FILE_NAME
    # -f (default file type; used if -j not called)
    if args.file_to_delete is not '' or args.jobfile_to_delete is '':
	if args.file_to_delete is None:
            args.file_to_delete = vdjpy.prompt_user('file to delete')
	filetype = 'projectFile'
    # -j (only used if specified)
    else:
	if args.jobfile_to_delete is None:
	    args.jobfile_to_delte = vdjpy.prompt_user('jobfile to delete')
	filetype = 'projectJobFile'
	# consolidate file name to args.file_to_delete no matter file type
	args.file_to_delete = args.jobfile_to_delete
    
    # get file_to_delete metadata
    files = vdjpy.get_project_files(project_uuid, filetype, {}, my_agave)
    file_metadata = vdjpy.get_file_metadata(files, args.file_to_delete) 
    if file_metadata is None:
        sys.exit()
   
    # change isDeleted to true
    file_metadata['value']['isDeleted'] = True

    # delete file via metadata update
    delete_resp = my_agave.meta.updateMetadata(uuid = file_metadata['uuid'],
					       body = json.dumps(file_metadata))

    # if -v
    if args.verbose:
        print json.dumps(delete_resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
    
    # if no -v
    else:
        print 'Deleted', args.file_to_delete, 'from project', args.project
