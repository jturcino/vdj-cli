#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib
import requests

system = 'data.vdjserver.org/'

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', default = None, nargs = '?')
    parser.add_argument('-n', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-y', '--file_type', dest = 'file_type', default = '', nargs = '?')
    parser.add_argument('-r', '--read_direction', dest = 'read_direction', default = '', nargs = '?')
    parser.add_argument('-t', '--tags', dest = 'tags', default = False, action = 'store_true')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    args = parser.parse_args()

    # UPLOAD FILE SETUP
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
    project_uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if project_uuid is None:
        sys.exit('Could not find specified project')
    kwargs['filePath'] = '/projects/' + project_uuid + '/files'

    # upload file
    upload = my_agave.files.importData(**kwargs)

    # UPDATE METADATA SETUP
    file_uuid = str(upload['uuid'])
    extras = ''
    
    # -y
    if args.file_type is not '':
        if args.file_type is None:
            args.file_type = vdjpy.prompt_user('file type')
        extras += '&vdjFileType=' + args.file_type

    # -r
    if args.read_direction is not '':
        if args.read_direction is None:
            args.read_direction = vdjpy.prompt_user('read_direction')
        extras += '&readDirection=' + args.read_direction

    # -t
    if args.tags:
        tag_string = vdjpy.prompt_user('tags as a comma-separated list')
        tag_string = urllib.quote(tag_string)
        extras += '&tags=' + tag_string

    # update metadata
    resp = vdjpy.update_metadata(project_uuid, args.file_name, file_uuid, extras)

    # if -v
    if args.verbose:
        print json.dumps(upload, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 
        print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now uploading', args.file_upload, 'at path', str(upload['path'])
