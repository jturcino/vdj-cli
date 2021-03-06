#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Make a directory on a remote system. System defaults to data.vdjserver.org. This command does not update metadata. Files uploaded to the created directory will not be visible on vdjserver.org')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to created directory. Do not append new directory name to the end of the path.')
    parser.add_argument('-d', '--dirname', dest = 'dirname', nargs = '?', help = 'name of directory to be created')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -d
    if args.dirname is None:
        args.dirname = vdjpy.prompt_user('new directory name')
    kwargs['body']  = {'action': 'mkdir', 'path': args.dirname}

    # mkdir
    mkdir = my_agave.files.manage(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(mkdir, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now creating directory', str(mkdir['name']), 'at', args.path 
