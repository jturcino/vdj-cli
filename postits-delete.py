#!/usr/bin/env python

import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nonce', dest = 'nonce', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # -n
    if args.nonce is None:
        args.nonce = vdjpy.prompt_user('nonce of postit')
    kwargs['nonce'] = args.nonce

    # delete postit
    postit_delete = my_agave.postits.delete(**kwargs)

    if postit_delete == {}:
        print 'successfully deleted postit', args.nonce
