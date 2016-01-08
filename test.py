#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
#parser.add_argument('-V','--veryVerbose', dest = 'veryVerbose',  type = bool, default = False, nargs = '?')
parser.add_argument('-V', '--veryverbose', dest = 'veryVerbose', action = 'store_true')
args = parser.parse_args()

if args.veryVerbose:
    print 'Activated: if args.veryVerbose'
    print 'args.veryVerbose is', args.veryVerbose

elif args.veryVerbose is True:
    print 'Activated: args.veryVerbose is True'
    print 'args.veryVerbose is', args.veryVerbose

elif args.veryVerbose is False:
    print 'Activated: args.verVerbose is False'
    print 'args.veryVerbose is', args.veryVerbose

else:
    print 'None activated.'
    print 'args.veryVerbose is', args.veryVerbose
