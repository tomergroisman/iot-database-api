import psycopg2
from flask import request

import services.constants as constants
from services.postgres import create_database, create_table, drop_database, drop_table


def create_database_api():
    """
    Create a new database

    - *body (req)*: {
        db_name? (string): The new database name default is default_db_name param
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        user, password, db_name, *_ = extract_data_from_body()

        if db_name is None:
            return "'db_name' parameter is mandatory", 400

        create_database(user, password, db_name)

        return f"'{db_name}' was created successfully"

    except psycopg2.errors.SyntaxError as e:
        return f'There was an issue with the provided parameters:\n{e}', 400

    except psycopg2.errors.DuplicateDatabase:
        return f"'{db_name}' is already created", 400


def drop_database_api(db_name: str):
    """
    Drop an existing database

    - *body (req)*: {
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        user, password, *_ = extract_data_from_body()

        drop_database(user, password, db_name)

        return f"'{db_name}' was dropped successfully"

    except psycopg2.errors.InvalidCatalogName:
        return f"'{db_name}' is not an existing database", 400


def create_table_api(db_name: str):
    """
    Create a new table in a database

    - *body (req)*: {
        table_name (string): the new table name
        columns: A list of column dictionaties: {name (string), data_type (string), length (number), constrains (list)}
        primary_keys: A list of primary keys (string)
        forign_keys: A list of forgin keys dictionaties: {name (string), reference (string)}
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        user, password, _, table_name, columns, primary_keys, forign_keys = extract_data_from_body()

        create_table(user, password, db_name, table_name, columns, primary_keys, forign_keys)

        return f"'{table_name}' was created successfully in '{db_name}' database"

    except psycopg2.errors.SyntaxError as e:
        return f'There was an issue with the provided parameters:\n{e}', 400

    except psycopg2.errors.DuplicateTable:
        return f"'{table_name}' is already exist in '{db_name}' database", 400


def drop_table_api(db_name: str, table_name: str):
    """
    Create a new table in a database

    - *body (req)*: {
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    user, password, *_ = extract_data_from_body()

    drop_table(user, password, db_name, table_name)

    return f"'{table_name}' was dropped successfully from '{db_name}' database"


def extract_data_from_body(
    default_user=constants.DEFAULT_USER,
    default_password=constants.DEFAULT_PASSWORD,
    default_db_name=None,
    default_table_name=None,
    default_columns=None,
    default_primary_keys=None,
    default_forign_keys=None

):
    body = request.get_json() or {}

    user = body.get('user', default_user)
    password = body.get('password', default_password)
    db_name = body.get('db_name', default_db_name)
    table_name = body.get('table_name', default_table_name)
    columns = body.get('columns', default_columns)
    primary_keys = body.get('primary_keys', default_primary_keys)
    forign_keys = body.get('forign_keys', default_forign_keys)

    return user, password, db_name, table_name, columns, primary_keys, forign_keys
