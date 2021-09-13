from flask import Blueprint

from services.api import (
  create_database_api,
  create_table_api,
  drop_database_api,
  drop_table_api,
  get_instances_api,
  init_database_api,
  insert_instance_api
)
from services.extarctors import extract_data_from_body

database = Blueprint('database', __name__)


@database.route('/', methods=['POST'])
def create_new_database():
    """
    POST /database
    Create a new database

    - *body (req)*: {
        db_name (string): The new database name
    }

    """
    db_name, *_ = extract_data_from_body()
    return create_database_api(db_name)


@database.route('/<db_name>', methods=['DELETE'])
def drop_selected_database(db_name: str):
    """
    DELETE /database/<db_name>
    Drop an existing database

    - *db_name* (string): The db name to drop
    """
    return drop_database_api(db_name)


@database.route('/<db_name>/table', methods=['POST'])
def create_new_table(db_name: str):
    """
    POST /database/<db_name>/table
    Create a new table in a database

    - *db_name* (string): The db name to create the table
    - *body (req)*: {
        table_name (string): the new table name
        columns (list[Column]): A list of column dictionaties
        primary_keys (list[string]): A list of primary keys
        forign_keys (list(ForignKey)): A list of forgin keys dictionaties
    }

    """
    _, table_name, columns, primary_keys, forign_keys, *_ = extract_data_from_body()
    return create_table_api(db_name, table_name, columns, primary_keys, forign_keys)


@database.route('/<db_name>/table/<table_name>', methods=['DELETE'])
def drop_selected_table(db_name: str, table_name: str):
    """
    DELETE /database/<db_name>/table/<table_name>
    Create a new table in a database

    - *db_name* (string): The db name to drop
    - *table_name* (string): The table name to drop
    """
    return drop_table_api(db_name, table_name)


@database.route('/init', methods=['POST'])
def init_new_database():
    """
    POST /database/init
    Initialize a new database and table

    - *body (req)*: {
        db_name (string): The new database name
        table_name (string): the new table name
        columns (list[Column]): A list of column dictionaties
        primary_keys (list[string]): A list of primary keys (optional)
        forign_keys (list(ForignKey)): A list of forgin keys dictionaties (optional)
    }

    """
    db_name, table_name, columns, primary_keys, forign_keys, *_ = extract_data_from_body()
    return init_database_api(db_name, table_name, columns, primary_keys, forign_keys)


@database.route('/<db_name>/table/<table_name>', methods=['POST'])
def insert_new_instance_to_selected_table(db_name: str, table_name: str):
    """
    POST /database/<db_name>/table/<table_name>
    Insert new instance to a table in a database

    - *db_name* (string): The db name to drop
    - *table_name* (string): The table name to drop
    - *body (req)*: {
        instance (Instance): The new instance to insert
    }

    """
    *_, instance = extract_data_from_body()
    return insert_instance_api(db_name, table_name, instance)


@database.route('/<db_name>/table/<table_name>', methods=['GET'])
def get_instances_from_selected_table(db_name: str, table_name: str):
    """
    GET /database/<db_name>/table/<table_name>
    Get instance from a table in a database

    - *db_name* (string): The db name to drop
    - *table_name* (string): The table name to drop
    - *query* (req): {
        columns (string): The columns to filter
        filter (string): PostgreSQL filter query
    }

    """
    return get_instances_api(db_name, table_name)
