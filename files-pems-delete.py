#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest = 'path', nargs = '?')
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = 'data.vdjserver.org', nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system')
    kwargs['systemId'] = args.systemID

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path')
    kwargs['filePath'] = args.path

    # delete permissions
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    pems_delete = my_agave.files.deletePermissions(**kwargs)

    if pems_delete is None:
        print 'Succesfully removed permissions for file at path', args.path
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(pems_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
