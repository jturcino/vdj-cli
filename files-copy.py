#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--system', dest = 'system', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-d', '--destination', dest = 'destination', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -s
    if args.system is None:
        args.system = vdjpy.prompt_user('system')

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # -d
    if args.destination is None:
        args.destination = vdjpy.prompt_user('destination of the file')
    kwargs['body']  = "{\"action\":\"copy\",\"path\": \"" + args.destination + "\"}"

    # copy file
    copy = vdjpy.manage_files(my_agave, args.system, kwargs)

    # if -v
    if args.verbose:
         print json.dumps(copy, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now copying', str(copy['name']), 'from', args.path, 'to', args.destination 
