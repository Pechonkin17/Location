from model import Reaction
from .db_session import db_session


@db_session
def create_reaction(session, user_id, location_id, text, like):
    reaction = Reaction(
        comment_text=text,
        like=like,
        location_id=location_id,
        user_id=user_id
    )
    session.add(reaction)
    session.commit()


@db_session
def find_liked_reactions_in_location(session, location_id):
    like_reactions = session.query(Reaction).filter_by(location_id=location_id, like=True).count()
    return like_reactions


@db_session
def find_disliked_reactions_in_location(session, location_id):
    dislike_reactions = session.query(Reaction).filter_by(location_id=location_id, like=False).count()
    return dislike_reactions


@db_session
def get_all_reactions_in_location(session, location_id):
    reactions = session.query(Reaction).filter_by(location_id=location_id).all()
    return reactions