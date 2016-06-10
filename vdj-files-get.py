#!/usr/bin/env python

import vdjpy
import argparse
import os.path
import sys


if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-n', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-f', '--file_download', dest = 'file_download', default = None, nargs = '?')
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    args = parser.parse_args()
    
    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if project_uuid is None:
        sys.exit('Cancelling command because of invalid project name')

    # -f
    if args.file_download is None:
        args.file_download = vdjpy.prompt_user('file to download')
    kwargs['sourcefilePath'] = '/projects/' + project_uuid + '/files/' + args.file_download

    # -n
    if args.file_name is None:
        args.file_name = args.file_download

    # make Agave object and download file
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    download = my_agave.files.downloadFromDefaultSystem(**kwargs)
    download.raise_for_status()

    # write correct contents to file
    with open(os.path.expanduser(args.file_name), 'w') as download_file:
        download_file.write(download.text)

    print 'Successfully downloaded', args.file_download, 'as', args.file_name, 'to the current directory.'
