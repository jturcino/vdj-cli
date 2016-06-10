#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()
    
    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if uuid is None:
        sys.exit()

    # -f
    if args.file_name is None:
        args.file_name = vdjpy.prompt_user('file name')
    kwargs['filePath'] = '/projects/' + uuid + '/files/' + args.file_name

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get history
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    history = my_agave.files.getHistoryOnDefaultSystem(**kwargs)
    print json.dumps(history, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
