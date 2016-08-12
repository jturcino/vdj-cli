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
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # make agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit()

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

    # build path and delete permissions
    pems_delete = my_agave.files.deletePermissions(systemId = 'data.vdjserver.org',
						   filePath = file_path)

    if pems_delete is None:
        print 'Succesfully removed permissions for file', args.file_name, 'in project', args.project
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(pems_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
