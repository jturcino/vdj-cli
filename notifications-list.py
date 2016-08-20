#!/usr/bin/env python

import vdjpy
import argparse
import json
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'List notification by associated uuid. If a notification uuid is given, more detailed information about that notification will be returned.')
    parser.add_argument('-n', '--notification_uuid', dest = 'notification_uuid', default = '', nargs = '?', help = 'uuid of notification')
    parser.add_argument('-a', '--associated_uuid', dest = 'associated_uuid', nargs = '?', help = 'uuid of associated object')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # IF NOTIFICATIONID, GET NOTIFICATION INFO, PRINT, AND EXIT
    if args.notification_uuid is not '':
	if args.notification_uuid is None:
	    args.notification_uuid = vdjpy.prompt_user('notification uuid')
	resp = my_agave.notifications.get(uuid = args.notification_uuid)
	print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
        sys.exit()

    # -a
    if args.associated_uuid is None:
        args.associated_uuid = vdjpy.prompt_user('associated uuid')
    kwargs['associatedUuid'] = args.associated_uuid

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # get notifications
    notifications = my_agave.notifications.list(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(notifications, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for item in notifications:
            print item['id']
