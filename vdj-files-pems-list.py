#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', default = 250, type = int, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', default = 0, type = int, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['systemId'] = 'data.vdjserver.org'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit()

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

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
    kwargs['filePath'] = vdjpy.build_vdj_path(project_uuid, args.file_name, filetype, extra_path)

    # list permissions
    permissions = my_agave.files.listPermissions(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(permissions, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in permissions:
            permission_string = item['username'] + ' '
            if item['permission']['read']:
                permission_string += 'r'
            if item['permission']['write']:
                permission_string += 'w'
            if item['permission']['execute']:
                permission_string += 'e'
            print permission_string
