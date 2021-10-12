from flask import Blueprint, Response, request
from routes.weather.plot import get_weather_measurements_plot
from routes.weather.utils import get_interval_query

from services.api import get_instances_api, init_database_api, insert_instance_api
from services.extarctors import extract_data_from_body

from .constants import (
    WEATHER_DB_NAME as db_name,
    WEATHER_TABLE_NAME as table_name,
    WEATHER_TABLE_STRUCTURE as table_structure
)

weather = Blueprint('weather', __name__)


@weather.route('/', methods=['POST'])
def create_weather_database():
    """
    POST /weather
    Create a new weather database and table

    """
    columns = table_structure.get('columns')
    return init_database_api(db_name, table_name, columns)


@weather.route('/insert', methods=['POST'])
def insert_weather_instance():
    """
    POST /weather/insert
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
    GET /weather
    Get instances from measurements table in the weather database

    - *query* (req): {
        columns (string): The columns to filter
        filter (string): PostgreSQL filter query
        start (string): Start date (dd-mm-yyy form)
        end (string): End date (dd-mm-yyy form)
    }

    """
    start = request.args.get('start')
    end = request.args.get('end')
    additional_query = get_interval_query(start, end)
    return get_instances_api(db_name, table_name, additional_query)


@weather.route('/plot', methods=['GET'])
def get_plot():
    """
    GET /weather/plot
    Plot instances from measurements table in the weather database

    - *query* (req): {
        columns (string): The columns to filter
        filter (string): PostgreSQL filter query
    }

    """
    plot = get_weather_measurements_plot()
    return Response(plot, mimetype='image/png')
