#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uuid', dest = 'uuid', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    kwargs = {}
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -u
    if args.uuid is None:
        args.uuid = vdjpy.prompt_user('uuid of item')
    kwargs['uuid'] = args.uuid

    # delete metadata
    metadata_delete = my_agave.meta.deleteMetadata(**kwargs)
    
     # deliver message
    if metadata_delete is None:
        print 'Successfully deleted metadata item', args.uuid
    else:
        print 'Deletion was not successfull. The message returned from the request was:\n' + json.dumps(metadata_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
