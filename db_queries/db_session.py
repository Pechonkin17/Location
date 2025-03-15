from functools import wraps

from model import Session


def db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session() as session:
            return func(session, *args, **kwargs)
    return wrapper