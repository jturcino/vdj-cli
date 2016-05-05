#!/usr/bin/env python

import argparse
import getpass
import vdjpy
import os.path
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

cache_dict = {"apisecret":"","apikey":"","username":"","access_token":"","refresh_token":"","created_at":"","expires_in":"","expires_at":""}
user_cache = '~/.vdjapi'
token_url = 'https://vdjserver.org:443/api/v1/token'
is_cache = False

def read_for_login(cache, key):
    with open(os.path.expanduser(cache), 'r') as cache_contents:
        cache_dict = json.load(cache_contents)
    return str(cache_dict[key])

def get_token(username, refresh, password):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if password is None: # refresh token
        auth = requests.auth.HTTPBasicAuth(username, refresh)
        resp = requests.put(token_url, auth = auth, verify = False)
    else: # create token
        auth = requests.auth.HTTPBasicAuth(username, password)
        resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    resp = resp.json()
    return resp

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required = False, dest = 'username', default = None, nargs = '?')
    parser.add_argument('-p', '--password', required = False, dest = 'password', default = None, nargs = '?')
    parser.add_argument('-r', '--refresh', required = False, dest = 'refresh', default = '', nargs = '?', type = str)
    args = parser.parse_args()

    # get username
    if args.username is None: # if no username given
        if os.path.isfile(os.path.expanduser(user_cache)) is True:
            with open(os.path.expanduser(user_cache), 'r') as contents:
                try:
                    cache_dict = json.load(contents)
                    args.username = cache_dict['username']
                    is_cache = True
                except ValueError:
                    print "Unexpected contents in " + user_cache
    if args.username is unicode('') or args.username is None:  
        args.username = unicode(vdjpy.prompt_user('username'))
    print 'Username:', args.username

    # if -r
    if args.refresh is not '':
        if args.refresh is None:
            if is_cache is False:
                args.refresh = vdjpy.prompt_user('refresh token')
            else:
                args.refresh = cache_dict['refresh_token']

    # if no -r
    else:
        args.password = getpass.getpass('Enter your password: ')

    # get token
    response = get_token(args.username, args.refresh, args.password)
    
    # insert correct values
    cache_dict['username'] = args.username
    cache_dict['access_token'] = response['result']['access_token']
    cache_dict['refresh_token'] = response['result']['refresh_token']
    cache_dict['expires_in'] = response['result']['expires_in']
    # grab time stamp from when submitted get_token for created_at
    # expires_at is created_at + expires_in
    
    # write to cache
    with open(os.path.expanduser(user_cache), 'w') as json_file:
        json.dump(cache_dict, json_file)

    print 'Access token is:', str(response['result']['access_token'])
    print 'Refresh token is:', str(response['result']['refresh_token'])
