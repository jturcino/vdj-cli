import json
import argparse
import vdjpy

if __name__ == '__main__':

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--systemID', dest = 'systemID', required = True)
    parser.add_argument('-v', '--verbose', dest = 'verbose', action = 'store_true')
    parser.add_argument('-z', '--accesstoken', dest = 'accesstoken', required = False, default = None, nargs = '?')
    parser.add_argument('-r', '--role', dest = 'role', required = True, default = None, nargs = '?')
    args = parser.parse_args()

    # get token
    if args.accesstoken is None:
        access_token = vdjpy.read_cache('access_token')
        if access_token is None:
            access_token = vdjpy.prompt_user('access_token')
    else:
        access_token = args.accesstoken

    # get role
    if args.role is not 'GUEST' or 'USER' or 'PUBLISHER' or 'ADMIN' or 'OWNER' or None:
        print 'Enter the role to set for the user. Valid roles are GUEST, USER, PUBLISHER, ADMIN, and OWNER:',
        args.role = raw_input('')

    my_agave = vdjpy.make_vdj_agave(access_token)
    role_update = my_agave.systems.updateRole(systemId = args.systemID, body = args.role)

    print json.dumps(role_update, sort_keys = True, indent = 4, separators = (',', ': '))

