import os
from dotenv import load_dotenv

from services.constants import DEFAULT_USER, DEFAULT_PASSWORD

load_dotenv()

_user = os.environ.get('POSTGRESQL_USER', DEFAULT_USER)
_password = os.environ.get('POSTGRESQL_PASSWORD', DEFAULT_PASSWORD)


def get_credentials():
    return dict(user=_user, password=_password)


def set_credentials(user: str = _user, password: str = _password):
    global _user, _password
    _user = user
    _password = password
