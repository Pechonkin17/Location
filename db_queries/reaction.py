from model import Reaction
from .db_session import db_session


@db_session
def create_reaction(session, user_id: int, location_id: int, text: str, like: bool):
    reaction = Reaction(
        comment_text=text,
        like=like,
        location_id=location_id,
        user_id=user_id
    )
    session.add(reaction)
    session.commit()


@db_session
def find_liked_reactions_in_location(session, location_id: int) -> list:
    like_reactions = session.query(Reaction).filter_by(location_id=location_id, like=True).count()
    return like_reactions


@db_session
def find_disliked_reactions_in_location(session, location_id: int) -> list:
    dislike_reactions = session.query(Reaction).filter_by(location_id=location_id, like=False).count()
    return dislike_reactions


@db_session
def get_all_reactions_in_location(session, location_id: int) -> list:
    reactions = session.query(Reaction).filter_by(location_id=location_id).all()
    return reactions