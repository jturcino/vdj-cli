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
    args = parser.parse_args()

    # cache and query
    projects_cache = './.vdjprojects'
    projects_query = '{"name":"project"}'

    # -p
    if args.project is None:
        args.project = vdjpy.prompt_user('project name')

    # read cache
    uuid = None
    if os.path.isfile(os.path.expanduser(projects_cache)) is True:
        with open(os.path.expanduser(projects_cache), 'r') as projects_file:
            projects_list = json.load(projects_file)
        projects_file.close()
        uuid = vdjpy.check_for_project_name(projects_list, args.project) 

    # make Agave object 
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # if no cache
    if uuid is None: 
        projects = my_agave.meta.listMetadata(q = projects_query, limit = 5000)
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
        files = my_agave.meta.listMetadata(q = files_query, limit = 5000)
        print json.dumps(files, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
