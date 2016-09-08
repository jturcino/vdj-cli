#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'List user permissions for a metadata object.')
    parser.add_argument('-u', '--uuid', dest = 'uuid', nargs = '?', help = 'uuid of metadata object')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # -u
    if args.uuid is None:
        args.uuid = vdjpy.prompt_user('uuid of item')
    kwargs['uuid'] = args.uuid

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # list permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_list = my_agave.meta.listMetadataPermissions(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(pems_list, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in pems_list:
            user_pems = ''
            if item['permission']['read'] is True:
                user_pems+='r'
            if item['permission']['write'] is True:
                user_pems+='w'
            print item['username'], user_pems
