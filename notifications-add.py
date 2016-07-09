#!/usr/bin/env python

import vdjpy
import json
import argparse

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--notification_uuid', dest = 'notification_uuid', default = '', nargs = '?')
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

    # if -f, use as body; otherwise build body from inputs
    if args.info_file is not None:
        body_contents = vdjpy.read_json(args.info_file)
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
