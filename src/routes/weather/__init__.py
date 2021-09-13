import psycopg2
from flask import Blueprint

from services.api import extract_data_from_body
from services.postgres import create_database, create_table
from services.constants import (
    DEFAULT_WEATHER_DB_NAME as db_name,
    DEFAULT_WEATHER_TABLE_NAME as table_name
)

weather = Blueprint('weather', __name__)


@weather.route('/', methods=['POST'])
def create_weather_database():
    """
    POST /weather/create
    Create a new weather database and table

    - *body (req)*: {
        table_name (string): the new table name
        columns (list[Column]): A list of column dictionaties
        primary_keys (list[string]): A list of primary keys
        forign_keys (list[ForignKey]): A list of forgin keys dictionaties
        user? (string): db user name, default is 'admin'
        password? (string): db user password, default is 'admin'
    }

    """
    try:
        user, password, *_, columns, primary_keys, forign_keys = extract_data_from_body()

        create_database(user, password, db_name)
        create_table(user, password, db_name, table_name, columns, primary_keys, forign_keys)
        return f"'{db_name}' database and '{table_name}' table were created successfully"

    except psycopg2.errors.DuplicateDatabase:
        return f"'{db_name}' is already created", 400


@weather.route('/add', methods=['POST'])
def add_weather_instance():
    """
    POST /weather/add
    Create a new weather instance

    """
    pass
