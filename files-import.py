#!/usr/bin/env python

import vdjpy
import argparse
import json

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Import a file to a remote file system. System defaults to data.vdjserver.org. This command does not update metadata. If you with the imported file to be visible on vdjserver.org, use the vdj files import command.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to destination directory')
    parser.add_argument('-u', '--import_url', dest = 'import_url', nargs = '?', help = 'url of file to import')
    parser.add_argument('-n', '--file_name', dest = 'file_name', nargs = '?', help = 'name of file once imported. Defaults to original name.')
    parser.add_argument('-y', '--file_type', dest = 'file_type', default = '', nargs = '?', help = 'filetype of file to be imported')
    parser.add_argument('-w', '--email_or_webhook', dest = 'email_or_webhook', default = '', nargs = '?', help = 'the email or webhook to notify upon completion')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # UPLOAD FILE SETUP
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -u
    if args.import_url is None:
        args.import_url = vdjpy.prompt_user('import url')
    kwargs['urlToIngest'] = args.import_url

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -n
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('file name after import')
    kwargs['fileName'] = args.file_name

    # -y
    if args.file_type is not '':
        if args.file_type is None:
            args.file_type = vdjpy.prompt_user('file type')
        kwargs['fileType'] = args.file_type

    # -w
    if args.email_or_webhook is not '':
        if args.email_or_webhook is None:
            args.email_or_webhook = vdjpy.prompt_user('email or webhook')
        kwargs['callbackURL'] = args.email_or_webhook


    # import file
    import_resp = my_agave.files.importData(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(import_resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 

    # if no -v
    else:
        print 'Now importing file from', str(import_resp['source']), 'to path', str(import_resp['path'])
