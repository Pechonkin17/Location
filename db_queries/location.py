from sqlalchemy import or_

from model import Location
from .db_session import db_session


@db_session
def create_location(session, name, description, category, user_id):
    location = Location(name=name, description=description, category=category, user_id=user_id)
    session.add(location)
    session.commit()


@db_session
def get_locations_db(session):
    locations = session.query(Location).all()
    return locations


@db_session
def find_location_by_id(session, location_id):
    location = session.query(Location).filter_by(id=location_id).first()
    return location


@db_session
def put_location_db(session, location):
    session.add(location)
    session.commit()


@db_session
def delete_location_by_id(session, location_id):
    location = session.get(Location, location_id)
    if location:
        session.delete(location)
        session.commit()


@db_session
def find_location_by_category(session, category):
    locations = session.query(Location).filter_by(category=category).all()
    return locations


@db_session
def search_location(session, db_query):
    results = session.query(Location).filter(or_(
        Location.name.ilike(f'%{db_query}%'),
        Location.description.ilike(f'%{db_query}%')
    )).all()
    return results