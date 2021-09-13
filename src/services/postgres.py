from postgresql_python.postgresql import PostgreSQL
from postgresql_python.types import Column, ForignKey, Instance

from services.constants import (
    DEFAULT_USER as user,
    DEFAULT_PASSWORD as password
)


def create_database(db_name: str):
    """
    Create a new database

    - *db_name*: Database name to create

    """
    postgres = PostgreSQL(user=user, password=password)
    postgres.create_database(db_name)
    postgres.disconnect()


def drop_database(db_name: str):
    """
    Create a new database

    - *db_name*: Database name to create

    """
    postgres = PostgreSQL(user=user, password=password)
    postgres.drop_database(db_name)
    postgres.disconnect()


def create_table(
    db_name: str,
    table_name: str,
    columns: list[Column],
    primary_keys: list[str],
    forign_keys: list[ForignKey]
):
    """
    Create a new table in a database

    - *db_name*: The database name
    - *table_name*: The new table name
    - *columns*: A list of column dictionaties
    - *primary_keys*: A list of primary keys
    - *forign_keys*: A list of forgin keys dictionaties

    """
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
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
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
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
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
    postgres.insert(table_name, instance)
    postgres.disconnect()


def get_instances(
    db_name: str,
    table_name: str,
    columns: str,
    filter_query: str
):
    """
    Create a new instance in a database table

    - *db_name*: The database name
    - *table_name*: The table name
    - *filter_query*: A PostgreSQL filter query

    """
    kwargs = dict(columns=columns, filter=filter_query)
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
    results = postgres.get(table_name, **kwargs)
    postgres.disconnect()
    return results
