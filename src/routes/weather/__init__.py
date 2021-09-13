import psycopg2
from flask import Blueprint, request, jsonify

from services.api import extract_data_from_body, get_instances_api
from services.postgres import create_database, create_table, get_instances, insert_instance

from .constants import (
    WEATHER_DB_NAME as db_name,
    WEATHER_TABLE_NAME as table_name,
    WEATHER_TABLE_STRUCTURE as table_structure
)

weather = Blueprint('weather', __name__)


@weather.route('/', methods=['POST'])
def create_weather_database():
    """
    POST /weather/create
    Create a new weather database and table

    - *body (req)*: {
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        user, password, *_ = extract_data_from_body()
        columns = table_structure.get('columns')

        create_database(user, password, db_name)
        create_table(user, password, db_name, table_name, columns)
        return f"'{db_name}' database and '{table_name}' table were created successfully"

    except psycopg2.errors.DuplicateDatabase:
        try:
            create_table(user, password, db_name, table_name, columns)
            return f"'{table_name}' table was created successfully"
        except psycopg2.errors.DuplicateTable:
            return f"'{table_name}' is already exist in '{db_name}' database", 400


@weather.route('/', methods=['GET'])
def get_weather_instances():
    """
    GET /weather/add
    Get instances from measurements table in the weather database

    - *query* (req): {
        columns (string): The columns to filter
        filter (string): PostgreSQL filter query
    }

    """
    return get_instances_api(db_name, table_name)


@weather.route('/insert', methods=['POST'])
def insert_weather_instance():
    """
    POST /weather/add
    Create a new weather instance

    - *body* (req): {
        instance (Instance): The instance to insert
    }

    """
    try:
        user, password, *_, instance = extract_data_from_body()

        insert_instance(user, password, db_name, table_name, instance)
        return f"{instance['values']} were added to '{table_name}' table successfully"

    except Exception as e:
        return f'There was an issue with the provided parameters:\n{e}', 400
