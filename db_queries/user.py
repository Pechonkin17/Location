from typing import List

from werkzeug.security import generate_password_hash, check_password_hash

from model import User
from .db_session import db_session


@db_session
def create_user(session, username: str, email: str, password: str):
    user = User(username=username, email=email, password=generate_password_hash(password))
    session.add(user)
    session.commit()


@db_session
def update_user(session, user: User):
    session.add(user)
    session.commit()


@db_session
def delete_user_by_id(session, user_id: int):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()


@db_session
def find_all_users(session) -> List[User]:
    users = session.query(User).all()
    return users


@db_session
def find_by_email(session, email: int) -> User:
    user = session.query(User).filter_by(email=email).first()
    return user


@db_session
def find_user_by_id(session, id: int) -> User:
    user = session.query(User).filter_by(id=id).first()
    return user


def check_password(password: str, email: str):
    user = find_by_email(email)
    if check_password_hash(user.password, password):
        return user
    else: -1


@db_session
def change_password(session, password: str, email: str):
    user = find_by_email(email)
    user.password = generate_password_hash(password)
    session.commit()