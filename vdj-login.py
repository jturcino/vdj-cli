#!/usr/bin/env python

import argparse
import getpass
import vdjpy
import requests.exceptions
import sys
import time

user_cache = '~/.vdjapi'
template_cache = './cache-template.json'
token_url = 'https://vdjserver.org:443/api/v1/token'
is_cache = False

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required = False, dest = 'username', default = None, nargs = '?')
    parser.add_argument('-p', '--password', required = False, dest = 'password', default = None, nargs = '?')
    parser.add_argument('-r', '--refresh', required = False, dest = 'refresh', default = '', nargs = '?', type = str)
    parser.add_argument('-s', '--save', required = False, dest = 'save', default = False, action = 'store_true')
    args = parser.parse_args()

    # get username and load cache if to be saved
    if args.username is None or args.save is True:
        cache_dict = vdjpy.read_json(user_cache)
        if cache_dict is None or cache_dict.get('username') is None or cache_dict.get('username') is unicode(''):
            args.username = vdjpy.prompt_user('username')
            if args.save is True:
                cache_dict = vdjpy.read_json(template_cache)
        else:
            is_cache = True
            args.username = cache_dict.get('username')
    print 'Username:', args.username

    # if -r, but no value given
    if args.refresh is None:
        if is_cache:
            args.refresh = cache_dict.get('refresh_token')
        else:
            args.refresh = vdjpy.prompt_user('refresh token')

    # if no -r and no -p given
    if args.refresh is '' and args.password is None:
        args.password = getpass.getpass('Enter your password: ')

    # get token
    try:
        response = vdjpy.get_token(args.username, args.refresh, args.password)
        current_time = int(time.time())
    except requests.exceptions.HTTPError:
        sys.exit('The username, password, or refresh token is not valid. Please try again.')

    # if -S, insert correct values and write to user_cache
    if args.save:
        cache_dict['username'] = args.username
        cache_dict['access_token'] = response['result']['access_token']
        cache_dict['refresh_token'] = response['result']['refresh_token']
        cache_dict['expires_in'] = response['result']['expires_in']
        cache_dict['created_at'] = current_time
        cache_dict['expires_at'] = time.ctime(current_time + response['result']['expires_in'])
        vdjpy.write_json(cache_dict, user_cache)

    # print tokens
    print 'Access token is:', str(response['result']['access_token'])
    print 'Refresh token is:', str(response['result']['refresh_token'])

