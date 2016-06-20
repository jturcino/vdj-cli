#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', default = None)
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None)
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.systemID is None:
        args.systemID = vdjpy.prompt_user('system ID')
    kwargs['systemId'] = args.systemID
    
    # delete system
    system_delete = my_agave.systems.delete(**kwargs)

    # deliver message
    if system_delete is None:
        print 'Successfully deleted system', args.systemID
    else:
        print 'Deletion was not successfull. The message returned from the request was:\n' + json.dumps(system_delete, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
