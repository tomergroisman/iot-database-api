import psycopg2
from flask import request
from postgresql_python.postgresql import PostgreSQL

import utils.constants as constants


def create_database(default_db_name: str):
    """
    Create a new database

    - *body (req)*: {
        db_name? (string): The new database name default is default_db_name param
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        db_name, user, password = _extract_data_from_body(default_db_name)

        postgres = PostgreSQL(user=user, password=password)
        postgres.create_database(db_name)
        postgres.disconnect()

        return f'{db_name} was created successfully'

    except psycopg2.errors.DuplicateDatabase:
        return f'{db_name} is already created', 400


def drop_database(default_db_name: str):
    """
    Drop an existing database

    - *body (req)*: {
        db_name? (string): The new database name default is default_db_name param
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        db_name, user, password = _extract_data_from_body(default_db_name)

        postgres = PostgreSQL(user=user, password=password)
        postgres.drop_database(db_name)
        postgres.disconnect()

        return f'{db_name} was dropped successfully'

    except psycopg2.errors.InvalidCatalogName:
        return f'{db_name} is not an existing database', 400


def _extract_data_from_body(
    default_db_name,
    default_user=constants.DEFAULT_USER,
    default_password=constants.DEFAULT_PASSWORD
):
    body = request.get_json()
    db_name = body.get('db_name', default_db_name)
    user = body.get('user', default_user)
    password = body.get('password', default_password)

    return db_name, user, password