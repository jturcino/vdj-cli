#!/usr/bin/env python

import json
import requests
from agavepy.agave import Agave
import argparse
import os.path
import getpass

def parse_response(resp):
    """Return access and refresh tokens from JSON-generated dictionary."""
    token_info = resp.json()
    token_dict = token_info['result']
    access_token = token_dict['access_token']
    refresh_token = token_dict['refresh_token']
    return (str(access_token), str(refresh_token))

def create(token_url, username, password):
    """Create a new authentication token at url with given username and password."""
    auth = requests.auth.HTTPBasicAuth(username, password)
    resp = requests.post(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

def refresh(token_url, username, refresh_token):
    """Refresh authentication token at url with given username and refresh token."""
    auth = requests.auth.HTTPBasicAuth(username, refresh_token)
    resp = requests.put(token_url, auth = auth, verify = False)
    resp.raise_for_status()
    return parse_response(resp)

def write_cache(file_path, access_token, refresh_token):
    """Replace access and refresh tokens in ~/.vdjapi with current versions."""
    if os.path.isfile(os.path.expanduser(file_path)) is True:
        with open(os.path.expanduser(file_path), 'r') as json_file:
            json_dict = json.load(json_file)
        json_file.close()
        json_dict['access_token'] = unicode(access_token)
        json_dict['refresh_token'] = unicode(refresh_token)
        with open(os.path.expanduser(file_path), 'w') as json_file:
            json.dump(json_dict, json_file)
        json_file.close()
    return

def read_cache(file_path, key):
    """Get the value corresponding to key. Defaults to given file, but uses input upon failure."""
    if os.path.isfile(os.path.expanduser(file_path)) is True:
        with open(os.path.expanduser(file_path), 'r') as json_file:
            json_dict = json.load(json_file)
        json_file.close()
        return str(json_dict[key])
    else:
        print 'No cache found'
        return None

def prompt_user(key):
    print 'Enter your', key.replace('_', ' ') + ':',
    return_key = raw_input('')
    return return_key

#######################################################################################

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
        args.username = read_cache(vdj_cache, 'username')
        if args.username is None:
            args.username = prompt_user('username')
    print 'Username:', args.username

    if args.refresh is '': # if no -r given
        if args.password is None:
            args.password = getpass.getpass('Enter your password: ') 
        (access_token, refresh_token) = create(token_url, args.username, args.password)
        print 'Successfully created token'

    else: # if -r given
        if args.refresh is None: # refresh token not specified
            args.refresh = read_cache(vdj_cache, 'refresh_token')
            if args.refresh is None:
                args.refresh = prompt_user('refresh_token')
        print 'Refresh token:', args.refresh
        (access_token, refresh_token) = refresh(token_url, args.username, args.refresh)
        print 'Successfully refreshed token'

    # cleaning up
    write_cache(vdj_cache, access_token, refresh_token)
    print 'Access token is:', access_token
    print 'Refresh token is:', refresh_token
