#!/usr/bin/env python

import vdjpy
import argparse

system = 'data.vdjserver.org/'

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-f', '--file_to_delete', dest = 'file_to_delete', default = None, nargs = '?')
    args = parser.parse_args()

    kwargs = {}
    kwargs['systemId'] = system

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, args.accesstoken)
    if project_uuid is None:
        sys.exit('Could not find specified project.')
    project_uuid = str(project_uuid)
    
    # -f
    if args.file_to_delete is None:
        args.file_to_delete = vdjpy.prompt_user('file to delete')
    
    # construct path
    kwargs['filePath'] = '/projects/' + project_uuid + '/files/' + args.file_to_delete

    # delete file
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    delete = my_agave.files.delete(**kwargs)

    if delete is None:
        print 'Successfully deleted', args.file_to_delete, 'at', kwargs['filePath']
