#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Rename a file on a remote system. System defaults to data.vdjserver.org. This command does not update metadata. If you wish the effects of this command to be visible on vdjserver.org, use the vdj files rename command.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file')
    parser.add_argument('-n', '--new_name', dest = 'new_name', nargs = '?', help = 'new name of file')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
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

    # -d
    if args.new_name is None:
        args.new_name = vdjpy.prompt_user('new name')
    kwargs['body']  = {'action': 'rename', 'path': args.new_name}

    # rename
    rename = my_agave.files.manage(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(rename, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now renaming file at', args.path, 'to', str(rename['name'])
