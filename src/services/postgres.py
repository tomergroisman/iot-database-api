from typing import Any
from postgresql_python.postgresql import PostgreSQL
from postgresql_python.types import Column, ForignKey, Instance


def create_database(user: str, password: str, db_name: str):
    """
    Create a new database

    - *user*: PostgreSQL user name
    - *password*: User's password
    - *db_name*: Database name to create

    """
    postgres = PostgreSQL(user=user, password=password)
    postgres.create_database(db_name)
    postgres.disconnect()


def drop_database(user: str, password: str, db_name: str):
    """
    Create a new database

    - *user*: PostgreSQL user name
    - *password*: User's password
    - *db_name*: Database name to create

    """
    postgres = PostgreSQL(user=user, password=password)
    postgres.drop_database(db_name)
    postgres.disconnect()


def create_table(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    columns: list[Column],
    primary_keys: list[str] = None,
    forign_keys: list[ForignKey] = None
):
    """
    Create a new table in a database

    - *user*: PostgreSQL user name
    - *password*: User's password
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
    user: str,
    password: str,
    db_name: str,
    table_name: str,
):
    """
    Create a new table in a database

    - *user*: PostgreSQL user name
    - *password*: User's password
    - *db_name*: The database name
    - *table_name*: The new table name

    """
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
    postgres.drop_table(table_name=table_name)
    postgres.disconnect()


def insert_instance(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    instance: Instance
):
    """
    Create a new instance in a database table

    - *user*: PostgreSQL user name
    - *password*: User's password
    - *db_name*: The database name
    - *table_name*: The table name
    - *instance*: The new instance data

    """
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
    postgres.insert(table_name, instance)
    postgres.disconnect()


def get_instances(
    user: str,
    password: str,
    db_name: str,
    table_name: str,
    filter_query: str
):
    """
    Create a new instance in a database table

    - *user*: PostgreSQL user name
    - *password*: User's password
    - *db_name*: The database name
    - *table_name*: The table name
    - *filter_query*: A PostgreSQL filter query

    """
    postgres = PostgreSQL(user=user, password=password, db_name=db_name)
    results = postgres.get(table_name, filter_query)
    postgres.disconnect()
    return results
