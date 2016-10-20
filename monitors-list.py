#!/usr/bin/env python

import argparse
import json
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'List available monitors. Results can be filtered by monitor ID, target system, and whether the monitor is active. If a monitor ID is given, more detailed information about that monitor will be returned.')
    parser.add_argument('-m', '--monitorID', dest = 'monitorID', default = '', nargs = '?', help = 'monitor ID')
    parser.add_argument('-s', '--target_system', dest = 'target_system', default = '', nargs = '?', help = 'only return monitors targeting the given system')
    parser.add_argument('-a', '--activeonly', dest = 'activeonly', default = False, action = 'store_true', help = 'list only active monitors')
    parser.add_argument('-i', '--inactiveonly', dest = 'inactiveonly', default = False, action = 'store_true', help = 'list only inactive monitors')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # IF MONITORID, GET MONITOR INFO, PRINT, AND EXIT
    if args.monitorID is not '':
	if args.monitorID is None:
	    args.monitorID = vdjpy.prompt_user('monitor ID')
	resp = my_agave.monitors.get(monitorId = args.monitorID)
	print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
	sys.exit()

    # IF NO MONITORID, LIST MONITORS
    # active/inactive
    if args.activeonly is True and args.inactiveonly is False:
        kwargs['active'] = True
    elif args.inactiveonly is True and args.activeonly is False:
        kwargs['active'] = False

    # target system
    if args.target_system is not '':
        if args.target_system is None:
            args.target_system = vdjpy.prompt_user('target system')
        kwargs['target'] = args.target_system

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get monitors
    monitors = my_agave.monitors.list(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(monitors, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for monitor in monitors:
            print str(monitor['id']) + '\t' + str(monitor['target'])
