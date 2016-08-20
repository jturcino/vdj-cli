#!/usr/bin/env python

import json
import argparse
import vdjpy
import sys

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser(description = 'Generate a preauthenticated URI for an API endpoint. postit URI can be limited to the number of uses and/or timeframe during which they are valid.')
    parser.add_argument('-f', '--description_file', dest = 'description_file', default = '', nargs = '?', help = 'file containing JSON postit description')
    parser.add_argument('-u', '--url', dest = 'url', nargs = '?', help = 'url invoked when the postit is used')
    parser.add_argument('-l', '--lifetime', dest = 'lifetime', default = 2592000, nargs = '?', help = 'lifetime of the postit in seconds')
    parser.add_argument('-x', '--max_uses', dest = 'max_uses', default = 25, nargs = '?', help = 'maximum number of times the postit may be used')
    parser.add_argument('-m', '--method', dest = 'method', default = 'GET', nargs = '?', help = 'HTTP method the postit uses (GET, POST, PUT, or DELETE). Defaults to GET.')
    parser.add_argument('-a', '--no_auth', dest = 'no_auth', action = 'store_true', help = 'does not pre-authenticate the URL')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # if -f
    if args.description_file is not '':
        if args.description_file is None:
            args.description_file = vdjpy.prompt_user('path to description file')
        body_contents = vdjpy.read_json(args.description_file)
        if body_contents is None:
            sys.exit('Not a valid file path or does not contain a valid app description.')
        kwargs['body'] = json.dumps(body_contents)

    # else, build body
    else:
        # -u
        if args.url is None:
            args.url = vdjpy.prompt_user('url of postit')
        kwargs['body'] = '{"url": "' + args.url + '"'
        
        # -x
        if args.max_uses is None:
            args.max_uses = vdjpy.prompt_for_integer('max number of uses', 25)
        kwargs['body'] += ', "maxUses": "' + str(args.max_uses) + '"'

        # -a
        no_auth = 'false'
        if args.no_auth:
            no_auth = 'true'
        kwargs['body'] += ', "noauth": ' + no_auth

        # -l
        if args.lifetime is None:
            args.lifetime = vdjpy.prompt_for_integer('lifetime in seconds', 2592000)
        kwargs['body'] += ', "lifetime": ' + str(args.lifetime)

        # -m
        if args.method is None:
            print 'Valid methods are as follows: \n\tGET \n\tPUT \n\tPOST \n\tDELETE'
            args.method = vdjpy.prompt_user('method')
        kwargs['body'] += ', "method": "' + args.method + '"}'

    # make postit
    postit = my_agave.postits.create(**kwargs)

    # if -v
    if args.verbose:
        print json.dumps(postit, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        print 'postit ID:', postit['postit'], '\nurl:', postit['url']
