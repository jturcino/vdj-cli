#!/usr/bin/env python

import argparse
import json
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'Toggle the availability of the system off. System admin privileges are required to disable a system.')
    parser.add_argument('-s', '--systemID', dest = 'systemID', nargs = '?', help = 'system ID')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}
    kwargs['body'] = {'action': 'DISABLE'}

    # -s
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID

    # disable app
    disable = my_agave.systems.manage(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(disable, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'Successfully disabled system', args.systemID
