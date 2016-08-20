#!/usr/bin/env python

import vdjpy
import argparse
import sys


if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Delete a file on a remote system. System defaults to data.vdjserver.org. This command does not update metadata. If you wish the file to be removed from a project on vdjserver.org, use the vdj files delete command.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file to be deleted')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system name')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path to the file')
    kwargs['filePath'] = args.path

    # delete file
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    files_delete = my_agave.files.delete(**kwargs)

    if files_delete is None:
        print 'Successfully deleted file at path', args.path
    else:
        print 'Deletion was not successfull. The message returned from the request was:\n' + json.dumps(files_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
