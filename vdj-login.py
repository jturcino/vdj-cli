#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import argparse
import os.path
import getpass
import sharedfunctions

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required = False, dest = 'username', default = None, nargs = '?')
    parser.add_argument('-p', '--password', required = False, dest = 'password', default = None, nargs = '?')
    parser.add_argument('-r', '--refresh', required = False, dest = 'refresh', default = '', nargs = '?', type = str)
    args = parser.parse_args()

    # url for pulling token
    token_url = 'https://vdjserver.org:443/api/v1/token'
    
    # path to information cache
    vdj_cache = '~/.vdjapi'

    # logic for arguments
    if args.username is None: # if no username given
        args.username = sharedfunctions.read_cache(vdj_cache, 'username')
        if args.username is None:
            args.username = sharedfunctions.prompt_user('username')
    print 'Username:', args.username

    if args.refresh is '': # if no -r given
        if args.password is None:
            args.password = getpass.getpass('Enter your password: ') 
        (access_token, refresh_token) = sharedfunctions.create(token_url, args.username, args.password)
        print 'Successfully created token'

    else: # if -r given
        if args.refresh is None: # refresh token not specified
            args.refresh = sharedfunctions.read_cache(vdj_cache, 'refresh_token')
            if args.refresh is None:
                args.refresh = sharedfunctions.prompt_user('refresh_token')
        print 'Refresh token:', args.refresh
        (access_token, refresh_token) = sharedfunctions.refresh(token_url, args.username, args.refresh)
        print 'Successfully refreshed token'

    # cleaning up
    sharedfunctions.write_cache(vdj_cache, access_token, refresh_token)
    print 'Access token is:', access_token
    print 'Refresh token is:', refresh_token
