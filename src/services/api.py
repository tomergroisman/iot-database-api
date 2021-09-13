import psycopg2
from flask import request, jsonify
from postgresql_python.types import Column, ForignKey, Instance

from services.extarctors import extract_data_from_body
from services.postgres import create_database, create_table, drop_database, drop_table, get_instances, insert_instance


def create_database_api(user: str, password: str, db_name: str):
    """
    Create a new database to PostgreSQL server and return a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name

    """
    try:
        if db_name is None:
            return "'db_name' parameter is mandatory", 400

        create_database(user, password, db_name)

        return f"'{db_name}' was created successfully"

    except psycopg2.errors.DuplicateDatabase:
        return f"'{db_name}' is already created", 400

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def drop_database_api(user: str, password: str, db_name: str):
    """
    Drop a database from PostgreSQL server and return a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name

    """
    try:
        drop_database(user, password, db_name)

        return f"'{db_name}' was dropped successfully"

    except psycopg2.errors.InvalidCatalogName:
        return f"'{db_name}' is not an existing database", 400


def create_table_api(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    columns: list[Column],
    primary_keys: list[str] = None,
    forign_keys: list[ForignKey] = None
):
    """
    Create a new table in a database and return a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *columns* (list[Column]): A list of column dictionaties
    - *primary_keys* (list[string]): A list of primary keys (optional)
    - *forign_keys* (list(ForignKey)): A list of forgin keys dictionaties (optional)

    """
    try:
        create_table(user, password, db_name, table_name, columns, primary_keys, forign_keys)

        return f"'{table_name}' was created successfully in '{db_name}' database"

    except psycopg2.errors.DuplicateTable:
        return f"'{table_name}' is already exist in '{db_name}' database", 400

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def drop_table_api(user: str, password: str, db_name: str, table_name: str):
    """
    Drop a table from a database and return a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name
    - *table_name* (string): The new table name

    """
    drop_table(user, password, db_name, table_name)

    return f"'{table_name}' was dropped successfully from '{db_name}' database"


def init_database_api(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    columns: list[Column],
    primary_keys: list[str] = None,
    forign_keys: list[ForignKey] = None
):
    """
    Create a new database and table

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *columns* (list[Column]): A list of column dictionaties
    - *primary_keys* (list[string]): A list of primary keys (optional)
    - *forign_keys* (list(ForignKey)): A list of forgin keys dictionaties (optional)

    """
    try:
        create_database(user, password, db_name)
        create_table(user, password, db_name, table_name, columns, primary_keys, forign_keys)
        return f"'{db_name}' database and '{table_name}' table were created successfully"

    except psycopg2.errors.DuplicateDatabase:
        try:
            create_table(user, password, db_name, table_name, columns, primary_keys, forign_keys)
            return f"'{table_name}' table was created successfully"
        except psycopg2.errors.DuplicateTable:
            return f"'{table_name}' is already exist in '{db_name}' database", 400


def insert_instance_api(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    instance: Instance
):
    """
    Create a new table in a database and return a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *instance* (Instance): The new instance to insert

    """
    try:
        insert_instance(user, password, db_name, table_name, instance)

        return f"{instance['values']} were added to '{table_name}' table successfully"

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def get_instances_api(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
):
    """
    Get instances from a table in a database and return it a response

    - *user* (string): db user name
    - *password* (string): db user password
    - *db_name* (string): The new database name
    - *table_name* (string): the new table name

    """
    try:
        columns = request.args.get('columns')
        filter_query = request.args.get('filter')

        results = get_instances(user, password, db_name, table_name, columns, filter_query)
        return jsonify(results)

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400
