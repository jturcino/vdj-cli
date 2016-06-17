#!/usr/bin/env python

import vdjpy
import argparse
import sys
import json


if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-f', '--file_to_delete', dest = 'file_to_delete', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')


    args = parser.parse_args()

    # make agave object
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    
    # get project uuid
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit('Could not find specified project')
    project_uuid = str(project_uuid)

    # -f
    if args.file_to_delete is None:
        args.file_to_delete = vdjpy.prompt_user('file to delete')
    
    # get file_to_delete metadata
    files = vdjpy.get_project_files(project_uuid, {}, my_agave)
    file_metadata = None
    for item in files:
        if str(item['value']['name']) == args.file_to_delete:
            file_metadata = item
    if file_metadata is None:
        sys.exit('Could not find specified file in project')
   
    # change isDeleted to true
    file_metadata['value']['isDeleted'] = True

    # delete file via metadata update
    kwargs = {}
    kwargs['uuid'] = str(file_metadata['uuid'])
    kwargs['body'] = file_metadata
#insert try/catch for HTTPError
    delete_resp = my_agave.meta.updateMetadata(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(delete_resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
    
    # if no -v
    else:
        print 'Deleted', args.file_to_delete, 'from project', args.project
