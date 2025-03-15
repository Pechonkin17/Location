from sqlalchemy import Column, Integer, String, ForeignKey

from .base import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(512), nullable=False)
    category = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    reactions = ForeignKey('reactions.id')