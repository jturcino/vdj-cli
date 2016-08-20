#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Remove a system from public use. Global admin privileges are required to unpublish a system.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?', help = 'system ID')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['body'] = {'action': 'UNPUBLISH'}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # unpublish system
    unpublish = my_agave.systems.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(unpublish, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully unpublished system', publish['id']
