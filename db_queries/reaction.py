from model import Session, Reaction


def create_reaction(user_id, location_id, text, like):
    with Session() as session:
        reaction = Reaction(
            comment_text=text,
            like=like,
            location_id=location_id,
            user_id=user_id
        )
        session.add(reaction)
        session.commit()


def find_liked_reactions_in_location(location_id):
    with Session() as session:
        like_reactions = session.query(Reaction).filter_by(location_id=location_id, like=True).count()
        return like_reactions


def find_disliked_reactions_in_location(location_id):
    with Session() as session:
        dislike_reactions = session.query(Reaction).filter_by(location_id=location_id, like=False).count()
        return dislike_reactions


def get_all_reactions_in_location(location_id):
    with Session() as session:
        reactions = session.query(Reaction).filter_by(location_id=location_id).all()
        return reactions