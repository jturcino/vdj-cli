#!/usr/bin/env python

import vdjpy
import argparse
import json
import os.path
import urllib
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--notification_uuid', dest = 'notification_uuid', nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make Agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -a
    if args.notification_uuid is None:
        args.notification_uuid = vdjpy.prompt_user('notification uuid')
    kwargs['uuid'] = args.notification_uuid

    # delete notifications
    notification_delete = my_agave.notifications.delete(**kwargs)

    # deliver message
    if notification_delete is None:
        print 'Successfully deleted notification', args.notification_uuid
    else:
        print 'Deletion was not successfull. The message returned from the request was:\n' + json.dumps(notification_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
