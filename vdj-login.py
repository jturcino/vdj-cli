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

    # url for pulling token
    token_url = 'https://vdjserver.org:443/api/v1/token'
    
    # logic for arguments
    if args.username is None: # if no username given
        args.username = vdjpy.read_cache('~/.vdjapi','username')
    print 'Username:', args.username

    if args.refresh is '': # if no -r given
        if args.password is None:
            args.password = getpass.getpass('Enter your password: ') 
        (access_token, refresh_token) = vdjpy.create(token_url, args.username, args.password)
        print 'Successfully created token'

    else: # if -r given
        if args.refresh is None: # refresh token not specified
            args.refresh = vdjpy.read_cache('refresh_token')
        print 'Refresh token:', args.refresh
        (access_token, refresh_token) = vdjpy.refresh(token_url, args.username, args.refresh)
        print 'Successfully refreshed token'

    # cleaning up
    vdjpy.write_cache(access_token, refresh_token)
    print 'Access token is:', access_token
    print 'Refresh token is:', refresh_token
