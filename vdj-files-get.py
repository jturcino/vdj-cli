#!/usr/bin/env python

import vdjpy
import argparse
import os.path
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-n', '--newfile_name', dest = 'newfile_name', default = '', nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    args = parser.parse_args()
    
    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['systemId'] = 'data.vdjserver.org'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit('')

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

    # -n; use args.file_name if flag not used
    if args.newfile_name is '':
	args.newfile_name = args.file_name
    elif args.newfile_name is None:
	args.newfile_name = vdjpy.prompt_user('name of file once downloaded')
    

    # get extra path
    project_files = vdjpy.get_project_files(project_uuid, filetype, {}, my_agave)
    file_metadata = vdjpy.get_file_metadata(project_files, args.file_name)
    if file_metadata is None: # exit if file not found
	sys.exit()
    try:
	extra_path = str(file_metadata['value']['relativeArchivePath']) + '/'
    except KeyError:
	extra_path = ''

    # download file

    kwargs['filePath'] = vdjpy.build_vdj_path(project_uuid, args.file_name, filetype, extra_path)
    download = my_agave.files.download(**kwargs)
    download.raise_for_status()

    # write correct contents to file
    with open(os.path.expanduser(args.newfile_name), 'w') as download_file:
        download_file.write(download.text)

    print 'Successfully downloaded', args.file_name, 'as', args.file_name, 'to the current directory.'
