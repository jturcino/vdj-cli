#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email_or_url', dest = 'email_or_url', default = None, nargs = '?')
    parser.add_argument('-a', '--associated_uuid', dest = 'associated_uuid', default = None, nargs = '?')
    parser.add_argument('-p', '--persistent', dest = 'persistent', default = False, action = 'store_true')
    parser.add_argument('-f', '--info_file', dest = 'info_file', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-v', '--verbose', dest = 'verbose', default = False, action = 'store_true')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # if -f
    if args.info_file is not None:
        kwargs['body'] = json.dumps(vdjpy.read_json(args.info_file))

    else:
        # -e
        if args.email_or_url is None:
            args.email_or_url = vdjpy.prompt_user('email or url')
        
        # -a
        if args.associated_uuid is None:
            args.associated_uuid = vdjpy.prompt_user('associated uuid')
   
        # -p
        persistent = 'false'
        if args.persistent:
            persistent = 'true'
  
        kwargs['body'] = "{\"url\": \"" + args.email_or_url + "\", \"event\": \"*\", \"associatedUuid\": \"" + args.associated_uuid + "\", \"persistent\": " + persistent + "}"

    # add notification
    add = my_agave.notifications.add(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(add, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Notification for uuid', args.associated_uuid, 'now', add['status']
