#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Copy a file from a location to another on a remote system. System defaults to data.vdjserver.org. This command does not update metadata. If you wish the copied file to be visible at vdjserver.org, use the vdj files copy command.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file to be copied')
    parser.add_argument('-d', '--destination', dest = 'destination', nargs = '?', help = 'path to copy\'s destination. Include the file name at the end of this path.')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('systemID')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -d
    if args.destination is None:
        args.destination = vdjpy.prompt_user('destination of the file')
    kwargs['body']  = {'action': 'copy', 'path': args.destination}

    # copy file
    copy = my_agave.files.manage(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(copy, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now copying', str(copy['name']), 'from', args.path, 'to', args.destination 
