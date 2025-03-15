from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String, nullable=False)
    subscribed = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)