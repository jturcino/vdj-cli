#!/usr/bin/env python

import vdjpy
import argparse
import json
import urllib

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Upload a file as a projectfile to data.vdjserver.org. This command updates metadata, and the uploaded file will be visible on vdjserver.org.')
    parser.add_argument('-p', '--project', dest = 'project', nargs = '?', help = 'name of the project destination')
    parser.add_argument('-f', '--file_upload', dest = 'file_upload', nargs = '?', help = 'name of the file to upload')
    parser.add_argument('-n', '--file_name', dest = 'file_name', nargs = '?', help = 'name of the file once uploaded. Defaults to original name.')
    parser.add_argument('-y', '--file_type', dest = 'file_type', default = '', nargs = '?', help = 'filetype of file to be uploaded')
    parser.add_argument('-r', '--read_direction', dest = 'read_direction', default = '', nargs = '?', help = 'read direction of genetic data. To be used for fasta/fastq files.')
    parser.add_argument('-t', '--tags', dest = 'tags', action = 'store_true', help = 'use to enter tags')
    parser.add_argument('-w', '--email_or_webhook', dest = 'email_or_webhook', default = '', nargs = '?', help = 'the email or webhook to notify upon completion')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # UPLOAD FILE SETUP
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['systemId'] = 'data.vdjserver.org'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit('Could not find specified project')
    kwargs['filePath'] = vdjpy.build_vdj_path(project_uuid, '', 'projectFile', '')

    # -f
    if args.file_upload is None:
        args.file_upload = vdjpy.prompt_user('file to upload')
    kwargs['fileToUpload'] = open(args.file_upload)

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
