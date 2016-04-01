#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', dest = 'project', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 5000, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # cache and query
    projects_cache = './.vdjprojects'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')

    # -l (for listMetadata)
    if args.limit is None:
        args.limit = vdjpy.prompt_user('project limit')
    kwargs['limit'] = args.limit

    # -o (for listMetadata)
    if args.offset is None:
        args.offset = vdjpy.prompt_user('offset value')
    kwargs['offset'] = args.offset

    # read cache
    uuid = None
    if os.path.isfile(os.path.expanduser(projects_cache)) is True:
        projects = vdjpy.read_json(projects_cache)
        uuid = vdjpy.check_for_project_name(projects, args.project) 

    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # if no cache
    if uuid is None: 
        projects = vdjpy.get_vdj_projects(args.accesstoken, 5000, 0) 
        uuid = vdjpy.check_for_project_name(projects, args.project) 
    

    # if args.project does not exist
    if uuid is None:
        print 'The project', args.project, 'does not exist. \nHere are your current projects and uuids:'
        for item in projects:
            print item['value']['name'] + '\t' + item['uuid']
    
    # if args.project exits
    else:
        uuid = str(uuid)
        files_query = '{' + '"name": { $in: ["projectFile", "projectJobFile"]}, "value.projectUuid": "' + uuid + '", "value.isDeleted": false}'
        files_query = urllib.quote(files_query)
        kwargs['q'] = files_query

        files = my_agave.meta.listMetadata(**kwargs)
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
