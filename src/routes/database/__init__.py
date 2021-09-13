from flask import Blueprint

from services.api import (
  create_database_api,
  create_table_api,
  drop_database_api,
  drop_table_api,
  get_instances_api,
  insert_instance_api
)

database = Blueprint('database', __name__)


"""
POST /database
Create a new database

"""
database.route('/', methods=['POST'])(create_database_api)


"""
DELETE /database/<db_name>
Drop an existing database

"""
database.route('/<db_name>', methods=['DELETE'])(drop_database_api)


"""
POST /database/<db_name>/table
Create a new table in a database

"""
database.route('/<db_name>/table', methods=['POST'])(create_table_api)


"""
DELETE /database/<db_name>/table/<table_name>
Create a new table in a database

"""
database.route('/<db_name>/table/<table_name>', methods=['DELETE'])(drop_table_api)


"""
GET /database/<db_name>/table/<table_name>
Get instance from a table in a database

"""
database.route('/<db_name>/table/<table_name>', methods=['GET'])(get_instances_api)


"""
POST /database/<db_name>/table/<table_name>
Insert new instance to a table in a database

"""
database.route('/<db_name>/table/<table_name>', methods=['POST'])(insert_instance_api)
