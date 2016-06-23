#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-u', '--username', dest = 'username', default = '', nargs = '?')
    parser.add_argument('-e', '--email', dest = 'email', default = '', nargs = '?')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    kwargs = {}
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)

    # -u
    if args.username is not '':
        if args.username is None:
            args.username = vdjpy.prompt_user('username')
        kwargs['username'] = args.username

    # -e NOT TRIGGERED IF -u
    elif args.email is not '':
        if args.email is None:
            args.email = vdjpy.prompt_user('email')
        kwargs['email'] = args.email

    # -l
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # -o
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset value', 0)
    kwargs['offset'] = args.offset

    # get profiles
    profiles = my_agave.profiles.list(**kwargs)

    # verbose/standard output
    if args.verbose is True:
        print json.dumps(profiles, sort_keys = True, indent = 4, separators = (',', ': '))
    else:
        for profile in profiles:
            print profile['username']
