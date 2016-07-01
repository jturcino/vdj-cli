#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--system', dest = 'system', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-d', '--dirname', dest = 'dirname', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
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
