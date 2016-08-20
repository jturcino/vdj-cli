#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Move a file from one location to another on a remote system. System defaults to data.vdjserver.org. This command does not update metadata. If you wish the effects of this command to be visible on vdjserver.org, use the vdj files move command.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?', help = 'system ID')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?', help = 'path to file to be moved')
    parser.add_argument('-d', '--destination', dest = 'destination', nargs = '?', help = 'path to file\'s destination. Include the file name at the end of the path.')
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
    if args.destination is None:
        args.destination = vdjpy.prompt_user('destination of the file')
    kwargs['body']  = {'action': 'move', 'path': args.destination}

    # move file
    move = my_agave.files.manage(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(move, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now moving', str(move['name']), 'from', args.path, 'to', args.destination 
