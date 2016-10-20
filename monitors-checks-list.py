#!/usr/bin/env python

import argparse
import json
import vdjpy
import sys

if __name__ == '__main__':
    
    # arguments
    parser = argparse.ArgumentParser(description = 'List checks for the given monitor. If a check ID is given, more detailed information about that check will be returned.')
    parser.add_argument('-m', '--monitorID', dest = 'monitorID', default = None, nargs = '?', help = 'monitor ID')
    parser.add_argument('-c', '--checkID', dest = 'checkID', default = '', nargs = '?', help = 'check ID')
#    parser.add_argument('-s', '--start_date', dest = 'start_date', default = '', nargs = '?', help = 'start date of the check in ISO 8601 format (ex. 2004-02-12T15:19:21+00:00)')
#    parser.add_argument('-e', '--end_date', dest = 'end_date', default = '', nargs = '?', help = 'end date of the check in ISO 8601 format (ex. 2004-02-12T15:19:21+00:00)')
    parser.add_argument('-r', '--result', dest = 'result', default = '', nargs = '?', help = 'filter by test result; valid values are PASSED, FAILED, and UNKNOWN')
    parser.add_argument('-l', '--limit', dest = 'limit', type = int, default = 250, nargs = '?', help = 'maximum number of results to return')
    parser.add_argument('-o', '--offset', dest = 'offset', type = int, default = 0, nargs = '?', help = 'number of results to skip from the start')
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true', help = 'verbose output')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', nargs = '?', help = 'access token')
    args = parser.parse_args()

    # make agave object and kwargs
    my_agave = vdjpy.make_vdj_agave(args.accesstoken)
    kwargs = {}

    # monitorID
    if args.monitorID is None:
        args.monitorID = vdjpy.prompt_user('monitor ID')
    kwargs['monitorId'] = args.monitorID

    # IF CHECKID, GET CHECK INFO, PRINT, AND EXIT
    if args.checkID is not '':
	if args.checkID is None:
	    args.checkID = vdjpy.prompt_user('check ID')
        kwargs['checkId'] = args.checkID
	resp = my_agave.monitors.getCheck(**kwargs)
	print json.dumps(resp, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))
	sys.exit()

    # IF NO CHECKID, LIST CHECKS
    # start date
#    if args.start_date is not '':
#        if args.start_date is None:
#	    args.start_date = vdjpy.prompt_user('start date in ISO 8601 format')
#	kwargs['startDate'] = args.start_date

    # end date
#    if args.end_date is not '':
#        if args.end_date is None:
#	    args.end_date = vdjpy.prompt_user('end date in ISO 8601 format')
#        kwargs['endDate'] = args.end_date

    # result
    if args.result is not '':
        if args.result is None:
	    print 'Valid results are PASSED, FAILED, and UNKNOWN'
	    args.result = vdjpy.prompt_user('result')
        kwargs['result'] = args.result

    # limit
    if args.limit is None:
        args.limit = vdjpy.prompt_for_integer('limit', 250)
    kwargs['limit'] = args.limit

    # offset
    if args.offset is None:
        args.offset = vdjpy.prompt_for_integer('offset', 0)
    kwargs['offset'] = args.offset

    # get checks
    checks = my_agave.monitors.listChecks(**kwargs)

    # if -v
    if args.verbose is True:
        print json.dumps(checks, default = vdjpy.json_serial, sort_keys = True, indent = 4, separators = (',', ': '))

    # if no -v
    else:
        for check in checks:
            print str(check['id']) + '\t' + str(check['result'])
