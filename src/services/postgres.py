from typing import List
from postgresql_python.postgresql import PostgreSQL
from postgresql_python.types import Column, ForignKey, Instance

from services.auth import get_credentials


def create_database(db_name: str):
    """
    Create a new database

    - *db_name*: Database name to create

    """
    credentials = get_credentials()
    postgres = PostgreSQL(**credentials)
    postgres.create_database(db_name)
    postgres.disconnect()


def drop_database(db_name: str):
    """
    Create a new database

    - *db_name*: Database name to create

    """
    credentials = get_credentials()
    postgres = PostgreSQL(**credentials)
    postgres.drop_database(db_name)
    postgres.disconnect()


def create_table(
    db_name: str,
    table_name: str,
    columns: List[Column],
    primary_keys: List[str],
    forign_keys: List[ForignKey]
):
    """
    Create a new table in a database

    - *db_name*: The database name
    - *table_name*: The new table name
    - *columns*: A list of column dictionaties
    - *primary_keys*: A list of primary keys
    - *forign_keys*: A list of forgin keys dictionaties

    """
    credentials = get_credentials()
    postgres = PostgreSQL(**credentials, db_name=db_name)
    postgres.create_table(
        table_name=table_name,
        columns=columns,
        primary_keys=primary_keys,
        forign_keys=forign_keys
    )
    postgres.disconnect()


def drop_table(
    db_name: str,
    table_name: str,
):
    """
    Create a new table in a database

    - *db_name*: The database name
    - *table_name*: The new table name

    """
    credentials = get_credentials()
    postgres = PostgreSQL(**credentials, db_name=db_name)
    postgres.drop_table(table_name=table_name)
    postgres.disconnect()


def insert_instance(
    db_name: str,
    table_name: str,
    instance: Instance
):
    """
    Create a new instance in a database table

    - *db_name*: The database name
    - *table_name*: The table name
    - *instance*: The new instance data

    """
    credentials = get_credentials()
    postgres = PostgreSQL(**credentials, db_name=db_name)
    postgres.insert(table_name, instance)
    postgres.disconnect()


def get_instances(
    db_name: str,
    table_name: str,
    columns: str,
    filter_query: str,
    order: str,
    limit: str,
    offset: str,
):
    """
    Create a new instance in a database table

    - *db_name*: The database name
    - *table_name*: The table name
    - *filter_query*: A PostgreSQL filter query
    - *order* (bool): Return the results in reverse order
    - *limit* (int): Limitation number of result
    - *offset* (int): Offset from the first instance

    """
    credentials = get_credentials()
    kwargs = dict(columns=columns, filter=filter_query, order=order, limit=limit, offset=offset)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    postgres = PostgreSQL(**credentials, db_name=db_name)
    results = postgres.get(table_name, **kwargs)
    postgres.disconnect()
    return results
