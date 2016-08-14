#!/usr/bin/env python

import vdjpy
import argparse
import json
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', nargs = '?')
    parser.add_argument('-r', '--recursive', dest = 'recursive', action = 'store_true')
    parser.add_argument('-n', '--file_name', dest = 'file_name', nargs = '?')
    parser.add_argument('-w', '--email_or_webhook', dest = 'email_or_webhook', default = '', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
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
