#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib

system = 'data.vdjserver.org/'

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', default = None, nargs = '?')
    parser.add_argument('-n', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    kwargs = {}
    kwargs['systemId'] = system

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')

    # -f
    if args.file_upload is None:
        args.file_upload = vdjpy.prompt_user('file to upload')
    kwargs['fileToUpload'] = open(args.file_upload)

    # -n
    if args.file_name is None:
        args.file_name = args.file_upload
    kwargs['fileName'] = args.file_name

    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # get uuid, exit if does not exist
    uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if uuid is None:
        sys.exit()
    kwargs['filePath'] = '/projects/' + uuid + '/files'

    # upload file
    upload = my_agave.files.importData(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(upload, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 

    # if no -v
    else:
        print 'Now uploading', args.file_upload, 'at path', str(upload['path'])
