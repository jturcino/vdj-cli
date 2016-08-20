#!/usr/bin/env python

import urllib
import argparse
import vdjpy
import json
import re

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'List metadata objects based on query. Queries must be valid JSON wrapped in single quotes. For example: \'{"owner": "some_username"}\'')
    parser.add_argument('-q', '--query', dest = 'query', type = str, nargs = '?', help = 'query used to search metadata')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
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

