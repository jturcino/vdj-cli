#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-d', '--dirname', dest = 'dirname', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()
    kwargs['sourcefilePath'] = '/projects/' + uuid + '/files'

    # -d
    if args.dirname is None:
        args.dirname = vdjpy.prompt_user('new directory name')
    kwargs['body']  = {'action': 'mkdir', 'path': args.dirname}

    # mkdir
    mkdir = my_agave.files.manageOnDefaultSystem(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(mkdir, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Now creating directory', str(mkdir['name']), 'at project', args.project 

    # NEED WORKING METADATA CALL
