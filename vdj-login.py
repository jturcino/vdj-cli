#!/usr/bin/env python

import argparse
import getpass
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required = False, dest = 'username', default = None, nargs = '?')
    parser.add_argument('-p', '--password', required = False, dest = 'password', default = None, nargs = '?')
    parser.add_argument('-r', '--refresh', required = False, dest = 'refresh', default = '', nargs = '?', type = str)
    args = parser.parse_args()

    # get username
    if args.username is None: # if no username given
        args.username = vdjpy.read_for_login('~/.vdjapi', 'username')
    print 'Username:', args.username

    # if no -r
    if args.refresh is '':
        if args.password is None:
            args.password = getpass.getpass('Enter your password: ')
        (access_token, refresh_token) = vdjpy.create(args.username, args.password)
        print 'Successfully created token'

    # if -r
    else:
        if args.refresh is None: # refresh token not specified
            args.refresh = vdjpy.read_for_login('~/.vdjapi', 'refresh_token')
        (access_token, refresh_token) = vdjpy.refresh(args.username, args.refresh)
        print 'Successfully refreshed token'

    print 'Access token is:', access_token
    print 'Refresh token is:', refresh_token
