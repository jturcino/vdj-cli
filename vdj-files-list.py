#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'List projectfiles and jobfiles for a project on data.vdjserver.org. Results can be filtered by projecfile or jobfile type. If a specific file name is given with the projectfile or jobfile flag, information about that file only will be displayed.')
    parser.add_argument('-p', '--project', dest = 'project', nargs = '?', help = 'name of project')
    parser.add_argument('-f', '--projectfile', dest = 'projectfile', default = '', nargs = '?', help = 'list only projectfiles or a specific projecfile')
    parser.add_argument('-j', '--jobfile', dest = 'jobfile', default = '', nargs = '?', help = 'list only jobfiles or a specific jobfile')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # cache and query
    projects_cache = './.vdjprojects'

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')
    project_uuid = vdjpy.get_uuid(args.project, my_agave)
    if project_uuid is None:
        sys.exit()

    # -l (for listMetadata)
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 5000)
    kwargs['limit'] = args.limit

    # -o (for listMetadata)
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # SET UP FILETYPE
    # -f
    if args.projectfile is not '' and args.jobfile is '':
        filetype = 'projectFile'
    # -j
    elif args.jobfile is not '' and args.projectfile is '':
        filetype = 'projectJobFile'
    else:
	filetype = None

    # get files for metadata
    files = vdjpy.get_project_files(project_uuid, filetype, kwargs, my_agave)

    # filter to one file if name specified; quit if file not found
    if filetype == 'projectFile' and args.projectfile is not None:
	files = vdjpy.get_file_metadata(files, args.projectfile)
    elif filetype == 'projectJobFile' and args.jobfile is not None:
	files = vdjpy.get_file_metadata(files, args.jobfile)
    if files is None:
	sys.exit()

    # if -v or specific file given
    if args.verbose is True or type(files) is not list:
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v and files is a list
    else:
        for item in files:
            print item['value']['name']
