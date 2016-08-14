#!/usr/bin/env python

import argparse
import json
import os.path
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appID', dest = 'appID', nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -f
    if args.appID is None:
        args.appID = vdjpy.prompt_user('app ID')
    kwargs['appId'] = args.appID
    
    # ERROR, NO JSON RETURNED; TEMPORARY FIX
    # publish app
    try:
        delete = my_agave.apps.delete(**kwargs)
    except ValueError:
        print 'Successfully deleted', args.appID

