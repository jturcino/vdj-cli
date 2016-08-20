#!/usr/bin/env python

import vdjpy
import argparse
import json
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Upload a file to a remote system. System defaults to data.vdjserver.org. This command does not update metadata. If you wish to see the uploaded file on vdjserver.org, use the vdj files upload command. Recursive file uploads supported.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to destination directory on remote system. Do not append the file name to the path.')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', nargs = '?', help = 'the file or directory to upload')
    parser.add_argument('-r', '--recursive', dest = 'recursive', action = 'store_true', help = 'upload file or directory recursively')
    parser.add_argument('-n', '--file_name', dest = 'file_name', nargs = '?', help = 'name of file once uploaded. File will retain original name if this flag is not used. Not supported in recursive file uploads.')
    parser.add_argument('-w', '--email_or_webhook', dest = 'email_or_webhook', default = '', nargs = '?', help = 'email or webhook to notify upon completion')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # UPLOAD FILE SETUP
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('destination path')
    kwargs['filePath'] = args.path

    # -f
    if args.file_upload is None:
        args.file_upload = vdjpy.prompt_user('file to upload')
    try:
        kwargs['fileToUpload'] = open(args.file_upload)
    except IOError:
	print args.file_upload, 'is a directory. Beginning recursive upload'
	args.recursive = True

    # -r
    if args.recursive:
        vdjpy.recursive_file_upload(args.file_upload, args.path, args.systemID, my_agave, args.verbose)
        sys.exit()

    # -n
    if args.file_name is None:
        args.file_name = args.file_upload
    kwargs['fileName'] = args.file_name

    # -w
    if args.email_or_webhook is not '':
        if args.email_or_webhook is None:
            args.email_or_webhook = vdjpy.prompt_user('email or webhook')
        kwargs['callbackURL'] = args.email_or_webhook

    # upload file
    upload = my_agave.files.importData(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(upload, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 

    # if no -v
    else:
        print 'Now uploading', args.file_upload, 'at path', args.path
