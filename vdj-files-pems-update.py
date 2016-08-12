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
    parser.add_argument('-u', '--username', dest = 'username', default = None, nargs = '?')
    parser.add_argument('-r', '--recursive', dest = 'recursive', default = False, action = 'store_true')
    parser.add_argument('-a', '--access', dest = 'access', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -r
    recursive = 'false'
    if args.recursive:
        recursive = 'true'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit()

    # -u
    if args.username is None:
        args.username = vdjpy.prompt_user('username to update')
    
    # -a
    if args.access is None:
        print 'Valid permission options are as follows: \n\tREAD \n\tWRITE \n\tEXECUTE \n\tREAD_WRITE \n\tREAD_EXECUTE \n\tWRITE_EXECUTE \n\tALL \n\tNONE'
        args.access = vdjpy.prompt_user('permission to set')

    # SET UP FILETYPE AND GET FILE NAME IN ARGS.FILE_NAME
    # -f (default)
    if args.file_name is not '' or args.jobfile_name is '':
        if args.file_name is None or '':
            args.file_name = vdjpy.prompt_user('file name')
        filetype = 'projectFile'
    # -j (only if flag given)
    else:
        if args.jobfile_name is None:
            args.jobfile_name = vdjpy.prompt_user('jobfile name')
        filetype = 'projectJobFile'
        args.file_name = args.jobfile_name
        # get metadata for extra path; exit if file not found
        project_files = vdjpy.get_project_files(project_uuid, filetype, {}, my_agave)
        file_metadata = vdjpy.get_file_metadata(project_files, args.file_name)
        if file_metadata is None:
            sys.exit()

    # if jobfile, get extra path; then build file path
    extra_path = ''
    if filetype == 'projectJobFile':
        extra_path += str(file_metadata['value']['relativeArchivePath']) + '/'
    file_path = vdjpy.build_vdj_path(project_uuid, args.file_name, filetype, extra_path)

    # build body and update permissions
    pems_update = my_agave.files.updatePermissions(systemId = 'data.vdjserver.org',
						   filePath = file_path,
						   body = {"username": args.username,
							   "permission": args.access,
							   "recursive": recursive})

    # if -v
    if args.verbose:
         print json.dumps(pems_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Permissions for', args.username, 'now set to \n\texecute:', pems_update[0]['permission']['execute'], '\n\tread:', pems_update[0]['permission']['read'], '\n\twrite:', pems_update[0]['permission']['write'], '\n\trecursive:', args.recursive
