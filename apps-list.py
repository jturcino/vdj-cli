#!/usr/bin/env python

import argparse
import json
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'List available apps. Results can be filtered by app ID, system, name, public, and private settings. See apps search for more specific requests. If an app ID is given, more detailed information about that app will be returned.')
    parser.add_argument('-a', '--appID', dest = 'appID', default = '', nargs = '?', help = 'application ID')
    parser.add_argument('-s', '--system', dest = 'system', default = '', nargs = '?', help = 'only return apps on the given system')
    parser.add_argument('-n', '--name', dest = 'name', default = '', nargs = '?', help = 'only return
 apps with the given name')
    parser.add_argument('-p', '--publiconly', dest = 'publiconly', default = False, action = 'store_true', help = 'list only public apps')
    parser.add_argument('-q', '--privateonly', dest = 'privateonly', default = False, action = 'store_true', help = 'list only private apps')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-n', '--name', dest = 'name', default = '', nargs = '?', help = 'only return apps with the given name')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # IF APPID, GET APP INFO, PRINT, AND EXIT
    if args.appID is not '':
	if args.appID is None:
	    args.appID = vdjpy.prompt_user('app ID')
	resp = my_agave.apps.get(appId = args.appID)
	print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
	sys.exit()

    # IF NO APPID, LIST APPS
    # public/private
    if args.publiconly is True and args.privateonly is False:
        kwargs['publicOnly'] = args.publiconly
    elif args.privateonly is True and args.publiconly is False:
        kwargs['privateOnly'] = args.privateonly

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get apps
    apps = my_agave.apps.list(**kwargs)

    # name
    if args.name is None:
        args.name = vdjpy.prompt_user('app name')
    if args.name:
        filtered = []
        for app in apps:
            if str(app['name']) == args.name:
                filtered.append(app)
        apps = filtered

    # system
    if args.system is None:
        args.system = vdjpy.prompt_user('system ID')
    if args.system:
        filtered = []
        for app in apps:
            if str(app['executionSystem']) == args.system:
                filtered.append(app)
        apps = filtered

    # if -v
    if args.verbose is True:
        print json.dumps(apps, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no args
    else:
        for app in apps:
            print str(app['id'])
