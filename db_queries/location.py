from sqlalchemy import or_

from model import Session, Location


def create_location(name, description, category, user_id):
    with Session() as session:
        location = Location(name=name, description=description, category=category, user_id=user_id)
        session.add(location)
        session.commit()


def get_locations_db():
    with Session() as session:
        locations = session.query(Location).all()
        return locations


def find_location_by_id(location_id):
    with Session() as session:
        location = session.query(Location).filter_by(id=location_id).first()
        return location


def put_location_db(location):
    with Session() as session:
        session.add(location)
        session.commit()


def delete_location_by_id(location_id):
    with Session() as session:
        location = session.get(Location, location_id)
        if location:
            session.delete(location)
            session.commit()


def find_location_by_category(category):
    with Session() as session:
        locations = session.query(Location).filter_by(category=category).all()
        return locations


def search_location(db_query):
    with Session() as session:
        results = session.query(Location).filter(or_(
            Location.name.ilike(f'%{db_query}%'),
            Location.description.ilike(f'%{db_query}%')
        )).all()
        return results