from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from .base import Base


class Reaction(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=True)
    like = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))