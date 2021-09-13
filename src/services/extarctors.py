from flask import request


def extract_data_from_body(
    default_db_name=None,
    default_table_name=None,
    default_columns=None,
    default_primary_keys=None,
    default_forign_keys=None,
    default_instance=None
):
    body = request.get_json() or {}

    db_name = body.get('db_name', default_db_name)
    table_name = body.get('table_name', default_table_name)
    columns = body.get('columns', default_columns)
    primary_keys = body.get('primary_keys', default_primary_keys)
    forign_keys = body.get('forign_keys', default_forign_keys)
    instance = body.get('instance', default_instance)

    return db_name, table_name, columns, primary_keys, forign_keys, instance
