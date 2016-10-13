#!/usr/bin/env python

import argparse
import vdjpy
import sys
import time

user_cache = '~/.vdjapi'

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Check the status of the current access token. If the token has expired, create a new token or refresh with vdj login.')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    args = parser.parse_args()

    # load cache
    cache_dict = vdjpy.read_json(user_cache)
    if cache_dict is None:
        sys.exit('Cache does not exist.')
    elif cache_dict.get('created_at') is None or cache_dict.get('expires_in') is None:
        sys.exit('Cache is improperly fomatted.')

    # calculate remaining time
    current_time = int(time.time())
    expiration_time = int(cache_dict.get('created_at')) + int(cache_dict.get('expires_in'))
    remaining_time = expiration_time - current_time

    # if after expiration, output that cache has expired
    if expiration_time <= current_time:
        print 'Cache has expired. Please refresh or create a new access token.'

    # longer output for valid cache
    elif args.verbose:
        print 'Username:', cache_dict.get('username'), \
	      '\nTime left:', remaining_time, \
	      '\nExpires at:', cache_dict.get('expires_at')

    # concise output for valid cache
    else:
        print 'Cache is valid. Expires in', remaining_time, 'seconds.'


