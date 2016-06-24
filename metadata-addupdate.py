#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uuid', dest = 'uuid', default = '', nargs = '?')
    parser.add_argument('-f', '--metadata_filepath', dest = 'metadata_filepath', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    kwargs = {}
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -f
    if args.metadata_filepath is None:
        args.metadata_filepath = vdjpy.prompt_user('path to metadata file')
    
    # open -f and use as body
    body_contents = vdjpy.read_json(args.metadata_filepath)
    if body_contents is None:
        sys.exit('Not a valid file path or does not contain a valid app description.')
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
