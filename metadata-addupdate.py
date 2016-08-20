#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Add or update a metadata object. If the uuid of existing metadata is given, the metadata will be updated; otherwise, a new piece of metadata will be created.')
    parser.add_argument('-u', '--uuid', dest = 'uuid', default = '', nargs = '?', help = 'uuid of metadata object')
    parser.add_argument('-f', '--metadata_file', dest = 'metadata_file', nargs = '?', help = 'file containing JSON metadata description')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    kwargs = {}
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -f
    if args.metadata_file is None:
        args.metadata_file = vdjpy.prompt_user('path to metadata file')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.metadata_file)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain valid JSON.')
    kwargs['body'] = json.dumps(body_contents)
    
    # if -u given, use update
    if args.uuid is not '':
        if args.uuid is None:
            args.uuid = vdjpy.prompt_user('uuid of item')
        kwargs['uuid'] = args.uuid
        resp = my_agave.meta.updateMetadata(**kwargs)
    
    # else, use add
    else:
        resp = my_agave.meta.addMetadata(**kwargs)

    # print resp
    print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
