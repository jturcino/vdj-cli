#!/usr/bin/env python

import vdjpy
import argparse
import json
import urllib
import sys

import os.path
from os import listdir
def recursive_file_upload(filepath, destfilepath, agave_object, systemID):
    filename = os.path.basename(filepath)
    if destfilepath[len(destfilepath) - 1] != '/':
        destfilepath += '/'
    if os.path.isdir(filepath) is True:
        agave_object.files.manage(systemId = systemID,
                                  filePath = destfilepath,
                                  body = {'action': 'mkdir',
                                          'path': filename})
        destfilepath += filename + '/'
        print 'made dir', filename, 'at', destfilepath
        for item in os.listdir(filepath):
            recursive_file_upload(filepath + '/' + item, destfilepath, agave_object, systemID)
    else:
        agave_object.files.importData(systemId = systemID,
                                      filePath = destfilepath,
                                      fileToUpload = open(filepath),
                                      fileName = filename)
        print 'uploaded file', filename, 'at', destfilepath
        return

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', default = None, nargs = '?')
    parser.add_argument('-r', '--recursive', dest = 'recursive', action = 'store_true')
    parser.add_argument('-n', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-w', '--email_or_webhook', dest = 'email_or_webhook', default = '', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
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
    if args.recursive is False:
        kwargs['fileToUpload'] = open(args.file_upload)

    # -r
    if args.recursive:
        recursive_file_upload(args.file_upload, args.path, my_agave, args.systemID)
        print 'uploaded', args.file_upload, 'recursively to', args.path
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
