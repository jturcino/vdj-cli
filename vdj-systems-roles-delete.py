import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', required = True)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        access_token = vdjpy.read_cache('access_token')
        if access_token is None:
            access_token = vdjpy.prompt_user('access_token')
    else:
        access_token = args.accesstoken

    my_agave = vdjpy.make_vdj_agave(access_token)
    roles_delete = my_agave.systems.deleteRoles(systemId = args.systemID)
    
    print json.dumps(roles_list, sort_keys = True, indent = 4, separators = (',', ': '))
