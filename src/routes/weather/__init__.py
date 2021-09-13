from flask import Blueprint

from services.api import extract_data_from_body, get_instances_api, init_database_api, insert_instance_api

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

    """
    columns = table_structure.get('columns')
    return init_database_api(db_name, table_name, columns)


@weather.route('/insert', methods=['POST'])
def insert_weather_instance():
    """
    POST /weather/add
    Create a new weather instance

    - *body* (req): {
        instance (Instance): The instance to insert
    }

    """
    *_, instance = extract_data_from_body()
    return insert_instance_api(db_name, table_name, instance)


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
