#!/usr/bin/env python

import vdjpy
import argparse
import sys


if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest = 'path', default = None, nargs = '?')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', default = None, nargs = '?')
    parser.add_argument('-s', '--system', dest = 'system', default = None, nargs = '?')
    args = parser.parse_args()

    kwargs = {}

    # -s
    if args.system is None:
        args.system = vdjpy.prompt_user('system name')
    kwargs['systemId'] = args.system

    # -p
    if args.path is None:
        args.path = vdjpy.prompt_user('path to the file')
    kwargs['filePath'] = args.path

    # delete file
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    delete = my_agave.files.delete(**kwargs)

    if delete is None:
        print 'Successfully deleted file at path', args.path
