from flask import Blueprint

from services.api import create_database, drop_database

weather = Blueprint('weather', __name__)


@weather.route('/database', methods=['POST'])
def create_weather_database():
    """
    POST /weather/database
    Create a new weather database

    """
    return create_database('weather')


@weather.route('/database', methods=['DELETE'])
def drop_weather_database():
    """
    DELETE /weather/database
    Drop an existing weather database

    """
    return drop_database('weather')


@weather.route('/database/<db_name>/table', methods=['DELETE'])
def create_weather_table():
    """
    DELETE /weather/database
    Drop an existing weather database

    """
    return drop_database('weather')


