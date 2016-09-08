#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Delete metadata permissions for all users.')
    parser.add_argument('-u', '--uuid', dest = 'uuid', nargs = '?', help = 'uuid of metadata object')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    kwargs = {}

    # -u
    if args.uuid is None:
        args.uuid = vdjpy.prompt_user('uuid')
    kwargs['uuid'] = args.uuid

    # delete permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_delete = my_agave.meta.deleteMetadataPermission(**kwargs)

    if pems_delete is None:
        print 'Succesfully removed permissions for metadata object', args.uuid
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(pems_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
