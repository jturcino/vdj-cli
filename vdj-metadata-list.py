#!/usr/bin/env python

import urllib
import argparse
import vdjpy
import json
import requests
import re

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', dest = 'query', type = str, default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # -q
    if args.query is None:
        args.query = vdjpy.prompt_user('metadata query')
        args.query = re.sub(r'^\'|\'$', '', args.query)
    args.query = urllib.quote(args.query)

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_user('project limit')
        args.limit = int(args.limit)

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_user('offset value')
        args.offset = int(args.offset)

    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    metadata = my_agave.meta.listMetadata(q = args.query, limit = args.limit, offset = args.offset)

    print json.dumps(metadata, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': ')) 

