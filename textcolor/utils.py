
def parse_db_uri(db_uri):
    params = {}
    db_type, uri = db_uri.split('://', 1)

    params['adapter'] = db_type

    user_pass, host_port_database = uri.split('@')

    params['user'], params['password'] = user_pass.split(':', 1)

    params['host'], port_database = host_port_database.split(':', 1)

    params['port'], params['database'] = port_database.split('/', 1)

    params['port'] = int(params['port'])

    return params