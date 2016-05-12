#!/usr/bin/env python

import argparse
import getpass
import vdjpy
import requests.exceptions
import sys
import time

cache_dict = {"apisecret":"","apikey":"","username":"","access_token":"","refresh_token":"","created_at":"","expires_in":"","expires_at":""}
user_cache = '~/.vdjapi'
token_url = 'https://vdjserver.org:443/api/v1/token'
is_cache = False

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required = False, dest = 'username', default = None, nargs = '?')
    parser.add_argument('-p', '--password', required = False, dest = 'password', default = None, nargs = '?')
    parser.add_argument('-r', '--refresh', required = False, dest = 'refresh', default = '', nargs = '?', type = str)
    args = parser.parse_args()

    # get username
    if args.username is None: # if no username given
        cache_dict = vdjpy.read_json(user_cache)
        try:
            args.username = cache_dict['username']
            is_cache = True
        except ValueError and TypeError:
            cache_dict = {u'username': u'', u'apikey': u'', u'access_token': u'', u'created_at': u'', 'expires_in': u'', u'apisecret': u'', u'expires_at': u'', u'refresh_token': u''} # eventually use template instead
    if args.username is unicode('') or args.username is None:
        args.username = unicode(vdjpy.prompt_user('username'))
    print 'Username:', args.username

    # if -r, but no value given
    if args.refresh is None:
        if is_cache is False:
            args.refresh = vdjpy.prompt_user('refresh token')
        else:
            args.refresh = cache_dict['refresh_token']

    # if no -r and no -p given
    if args.refresh is '' and args.password is None:
        args.password = getpass.getpass('Enter your password: ')

    # get token
    try:
        response = vdjpy.get_token(args.username, args.refresh, args.password)
        current_time = int(time.time())
    except requests.exceptions.HTTPError:
        if args.password is None:
            sys.exit('The refresh token is not valid. Please try again without the refresh flag.')

    # insert correct values
    cache_dict['username'] = args.username
    cache_dict['access_token'] = response['result']['access_token']
    cache_dict['refresh_token'] = response['result']['refresh_token']
    cache_dict['expires_in'] = response['result']['expires_in']
    cache_dict['created_at'] = current_time
    cache_dict['expires_at'] = time.ctime(current_time + response['result']['expires_in'])

    # write to cache
    vdjpy.write_json(cache_dict, user_cache)

    print 'Access token is:', str(response['result']['access_token'])
    print 'Refresh token is:', str(response['result']['refresh_token'])

