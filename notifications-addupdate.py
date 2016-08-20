#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Add or update a notification object. If the uuid of an existing notification is given, the notification will be updated; otherwise, a new notification will be created.')
    parser.add_argument('-u', '--notification_uuid', dest = 'notification_uuid', default = '', nargs = '?', help = 'uuid of notification object')
    parser.add_argument('-f', '--description_file', dest = 'description_file', nargs = '?', help = 'file containing JSON notification description. Replaces use of -e, -a, and -p flags.')
    parser.add_argument('-a', '--associated_uuid', dest = 'associated_uuid', nargs = '?', help = 'uuid of associated object')
    parser.add_argument('-e', '--email_or_url', dest = 'email_or_url', nargs = '?', help = 'email or url to be notified')
    parser.add_argument('-p', '--persistent', dest = 'persistent', action = 'store_true', help = 'keeps notification active for many uses')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # if -f, use as body; otherwise build body from inputs
    if args.description_file is not None:
        body_contents = vdjpy.read_json(args.description_file)
        if body_contents is None:
            sys.exit('Not a valid file path or does not contain a valid notification description.')
        kwargs['body'] = json.dumps(body_contents)

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

    # update notification if args.notification_uuid; otherwise create new
    if args.notification_uuid is not '':
        if args.notification_uuid is None:
            args.notification_uuid = vdjpy.prompt_user('notification uuid')
        kwargs['uuid'] = args.notification_uuid
        add_update = my_agave.notifications.update(**kwargs)
    
    else:
        add_update = my_agave.notifications.add(**kwargs)

    # if -v
    if args.verbose:
         print json.dumps(add_update, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'notification uuid:', add_update['id'], '\nassociated uuid:', add_update['associatedUuid'], '\nurl:', add_update['url']
