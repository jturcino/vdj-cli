#!/usr/bin/env python

from datetime import datetime
import vdjpy
from datetime import datetime
import json

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

access_token = vdjpy.read_cache('access_token')
my_agave = vdjpy.make_vdj_agave(access_token)
apps = my_agave.apps.list()

for app in apps:
    print 'App:', app['id']
    print '\tLast modified', json.dumps(app['lastModified'], default=json_serial)
