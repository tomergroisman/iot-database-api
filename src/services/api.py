import psycopg2
from flask import request, jsonify
from typing import List
from postgresql_python.types import Column, ForignKey, Instance

from services.postgres import (
    create_database,
    create_table,
    drop_database,
    drop_table,
    get_instances,
    insert_instance
)


def create_database_api(db_name: str):
    """
    Create a new database to PostgreSQL server and return a response

    - *db_name* (string): The new database name

    """
    try:
        if db_name is None:
            return "'db_name' parameter is mandatory", 400

        create_database(db_name)

        return f"'{db_name}' was created successfully"

    except psycopg2.errors.DuplicateDatabase:
        return f"'{db_name}' is already created", 400

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def drop_database_api(db_name: str):
    """
    Drop a database from PostgreSQL server and return a response

    - *db_name* (string): The new database name

    """
    try:
        drop_database(db_name)

        return f"'{db_name}' was dropped successfully"

    except psycopg2.errors.InvalidCatalogName:
        return f"'{db_name}' is not an existing database", 400


def create_table_api(
    db_name: str,
    table_name: str,
    columns: List[Column],
    primary_keys: List[str] = None,
    forign_keys: List[ForignKey] = None
):
    """
    Create a new table in a database and return a response

    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *columns* (List[Column]): A list of column dictionaties
    - *primary_keys* (List[string]): A list of primary keys (optional)
    - *forign_keys* (List(ForignKey)): A list of forgin keys dictionaties (optional)

    """
    try:
        print(columns)
        create_table(db_name, table_name, columns, primary_keys, forign_keys)

        return f"'{table_name}' was created successfully in '{db_name}' database"

    except psycopg2.errors.DuplicateTable:
        return f"'{table_name}' is already exist in '{db_name}' database", 400

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def drop_table_api(db_name: str, table_name: str):
    """
    Drop a table from a database and return a response

    - *db_name* (string): The new database name
    - *table_name* (string): The new table name

    """
    try:
        drop_table(db_name, table_name)

        return f"'{table_name}' was dropped successfully from '{db_name}' database"

    except psycopg2.errors.UndefinedTable:
        return f"'{table_name}' is not exist in '{db_name}' database"


def init_database_api(
    db_name: str,
    table_name: str,
    columns: List[Column],
    primary_keys: List[str] = None,
    forign_keys: List[ForignKey] = None
):
    """
    Create a new database and table

    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *columns* (List[Column]): A list of column dictionaties
    - *primary_keys* (List[string]): A list of primary keys (optional)
    - *forign_keys* (List(ForignKey)): A list of forgin keys dictionaties (optional)

    """
    try:
        create_database(db_name)
        create_table(db_name, table_name, columns, primary_keys, forign_keys)
        return f"'{db_name}' database and '{table_name}' table were created successfully"

    except psycopg2.errors.DuplicateDatabase:
        try:
            create_table(db_name, table_name, columns, primary_keys, forign_keys)
            return f"'{table_name}' table was created successfully"
        except psycopg2.errors.DuplicateTable:
            return f"'{table_name}' is already exist in '{db_name}' database", 400


def insert_instance_api(
    db_name: str,
    table_name: str,
    instance: Instance
):
    """
    Create a new table in a database and return a response

    - *db_name* (string): The new database name
    - *table_name* (string): The new table name
    - *instance* (Instance): The new instance to insert

    """
    try:
        insert_instance(db_name, table_name, instance)

        return f"{instance['values']} were added to '{table_name}' table successfully"

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400


def get_instances_api(
    db_name: str,
    table_name: str,
    additional_filters: str,
):
    """
    Get instances from a table in a database and return it a response

    - *db_name* (string): The new database name
    - *table_name* (string): the new table name
    - *additional_filters* (string): Additional filter query

    """
    try:
        columns = request.args.get('columns')
        filter_query = request.args.get('filter')

        if additional_filters is not None:
            if filter_query is not None:
                filter_query += f" AND {additional_filters}"
            else:
                filter_query = additional_filters

        results = get_instances(db_name, table_name, columns, filter_query)
        return jsonify(results)

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400
