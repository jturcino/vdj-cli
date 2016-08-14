#!/usr/bin/env python

import urllib
import argparse
import vdjpy
import json
import re

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', dest = 'query', type = str, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # -q
    if args.query is None:
        args.query = vdjpy.prompt_user('metadata query')
        args.query = re.sub(r'^\'|\'$', '', args.query)
    args.query = urllib.quote(args.query)
    kwargs['q'] = args.query

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    metadata = my_agave.meta.listMetadata(**kwargs)

    print json.dumps(metadata, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 

