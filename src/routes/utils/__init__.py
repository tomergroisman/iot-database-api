import os
from flask import Blueprint, request
from dotenv import load_dotenv

from services.auth import set_credentials

load_dotenv()

utils = Blueprint('utils', __name__)


@utils.route('/health-check', methods=['GET'])
def health_check():
    """
    Health check
    Response is "Healthy" if server is up and running
    """
    return 'Healthy'


@utils.route('/config', methods=['POST'])
def config():
    """
    Reconfig the server

    - *body (req)*: {
        user (string): The PostgreSQL user name
        password (string): The PostgreSQL password
    }
    """
    auth_key = request.headers.get('Authorization')

    if os.environ.get('CONFIG_KEY') == auth_key:
        body = request.get_json()

        user = body.get('user')
        password = body.get('password')

        kwargs = dict(user=user, password=password)
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        set_credentials(**kwargs)

        return f'Successfully set credentials: {", ".join(kwargs.keys())}'
    return 'Auth key is not valid', 401
