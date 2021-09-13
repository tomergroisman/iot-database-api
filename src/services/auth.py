from services.constants import DEFAULT_USER, DEFAULT_PASSWORD

_user = DEFAULT_USER
_password = DEFAULT_PASSWORD


def get_credentials():
    return dict(user=_user, password=_password)


def set_credentials(user: str = _user, password: str = _password):
    global _user, _password
    _user = user
    _password = password
