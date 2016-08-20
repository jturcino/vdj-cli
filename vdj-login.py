#!/usr/bin/env python

import argparse
import getpass
import vdjpy
import requests.exceptions
import sys
import time

user_cache = '~/.vdjapi'
template_cache = './cache-template.json'

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Authenticate a user by retrieving a new access and refresh token. If the refresh flag is used, the new tokens are retrieved using the refresh token in the user\'s cache (~/.vdjapi), or one supplied by the user. If the save flag is used, the new tokens are cached.')
    parser.add_argument('-u', '--username', dest = 'username', nargs = '?', help = 'user to authenticate')
    parser.add_argument('-p', '--password', dest = 'password', nargs = '?', help = 'password of the user')
    parser.add_argument('-r', '--refresh', dest = 'refresh', default = '', nargs = '?', help = 'use cached refresh token or one supplied by the user')
    parser.add_argument('-s', '--save', dest = 'save', action = 'store_true', help = 'cache tokens once retrieved')
    args = parser.parse_args()

    # load cache
    cache_dict = vdjpy.read_json(user_cache)
    if cache_dict is None:
	if args.save:
	    cache_dict = vdjpy.read_json(template_cache)
	else:
	    cache_dict = {}

    # -u
    if args.username is None:
	args.username = cache_dict.get('username')
	if args.username is None or args.username == unicode(''):
	    print 'Username in cache does not exist or is empty'
	    args.username = vdjpy.prompt_user('username')

    # -r
    if args.refresh is None:
	args.refresh = cache_dict.get('refresh_token')
	if args.refresh is None or args.refresh == unicode(''):
	    print 'Refresh token in cache does not exist or is empty'
	    args.refresh = vdjpy.prompt_user('refresh token')

    # -p
    if args.refresh is '' and args.password is None:
	args.password = getpass.getpass('Enter password: ')

    # get token
    try:
        response = vdjpy.get_token(args.username, args.refresh, args.password)
        current_time = int(time.time())
    except requests.exceptions.HTTPError:
        sys.exit('The username, password, or refresh token is not valid. Please try again.')

    # if -s, insert correct values and write to user_cache
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

