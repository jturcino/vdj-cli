#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--system', dest = 'system', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?')
    parser.add_argument('-d', '--destination', dest = 'destination', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.system is None:
        args.system = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.system

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
