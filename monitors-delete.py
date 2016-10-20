#!/usr/bin/env python

import argparse
import json
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Delete a monitor. This action cannot be undone.')
    parser.add_argument('-m', '--monitorID', dest = 'monitorID', nargs = '?', help = 'monitor ID')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.monitorID is None:
        args.monitorID = vdjpy.prompt_user('monitor ID')
    kwargs['monitorId'] = args.monitorID
    
    # delete monitor
    monitor_delete = my_agave.monitors.delete(**kwargs)

    # deliver message
    if monitor_delete is None:
        print 'Successfully deleted monitor', args.monitorID
    else:
        print 'Deletion was not successfull. The message returned from the request was:\n' + json.dumps(monitor_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
