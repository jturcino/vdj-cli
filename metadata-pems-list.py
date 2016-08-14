#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uuid', dest = 'uuid', nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
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
    pems = my_agave.meta.listMetadataPermissions(**kwargs)

    # -v
    if args.verbose:
        print json.dumps(pems, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in pems:
            print item['username'], '\n\t read:', item['permission']['read'], '\n\twrite:', item['permission']['write']
