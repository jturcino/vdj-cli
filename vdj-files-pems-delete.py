#!/usr/bin/env python

import vdjpy
import json
import argparse
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_name', dest = 'file_name', default = '', nargs = '?')
    parser.add_argument('-j', '--jobfile_name', dest = 'jobfile_name', default = '', nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['systemId'] = 'data.vdjserver.org'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project')
    uuid = vdjpy.get_uuid(args.project, my_agave)
    if uuid is None:
        sys.exit()

    # -f
    if args.file_name is None or args.jobfile_name is '':
        args.file_name = vdjpy.prompt_user('file name')

    # -j (only if no -f)
    if args.jobfile_name is None and args.file_name is '':
        args.jobfile_name = vdjpy.prompt_user('jobfile name')
   
    # build path
    kwargs['filePath'] = vdjpy.build_vdj_path(uuid, args.file_name, args.jobfile_name)

    # delete permissions
    pems_delete = my_agave.files.deletePermissions(**kwargs)

    if pems_delete is None:
        print 'Succesfully removed permissions for file', args.file_name, 'in project', args.project
    else:
        print 'Permission removal was not successfull. The message returned from the request was:\n' + json.dumps(pems_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
