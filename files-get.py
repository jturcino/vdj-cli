#!/usr/bin/env python

import vdjpy
import argparse
import os.path
import sys
import requests.exceptions

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Download a file from a remote system. System defaults to data.vdjserver.org. Recursive file downloads supported.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file or directory on remote system')
    parser.add_argument('-r', '--recursive', dest = 'recursive', action = 'store_true', help = 'download file or directory recursively')
    parser.add_argument('-n', '--newfile_name', dest = 'newfile_name', default = '', nargs = '?', help = 'name of the file once downloaded. File will retain original name if this flag is not used. Not supported in recursive file downloads.')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()
    
    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.systemID is None:
	args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
	args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # get basename from path
    if args.path[len(args.path) - 1] == '/':
	args.path = args.path[:len(args.path) - 1]
    file_name = os.path.basename(args.path)

    # -n; use file_name if flag not used
    if args.newfile_name is '':
	args.newfile_name = file_name
    elif args.newfile_name is None:
	args.newfile_name = vdjpy.prompt_user('name of file once downloaded')
    
    # download file if not recursive; catch if user tries to download directory
    if args.recursive is False:
        try:
            download = my_agave.files.download(**kwargs)
        except requests.exceptions.HTTPError:
            print file_name, 'is a directory. Beginning recursive download.'
            args.recursive = True

    # if recursive, download (not using else becuase try/except above may chance args.recursive)
    if args.recursive is True:
        vdjpy.recursive_file_download(args.path, '.', args.systemID, my_agave)
        sys.exit()

    # write contents to file
    download.raise_for_status()
    with open(os.path.expanduser(args.newfile_name), 'w') as download_file:
        download_file.write(download.text)

    print 'Successfully downloaded', file_name, 'as', args.newfile_name
