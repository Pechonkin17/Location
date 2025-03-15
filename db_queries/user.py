from werkzeug.security import generate_password_hash, check_password_hash


from model import Session, User


def create_user(username, email, password):
    with Session() as session:
        user = User(username=username, email=email, password=generate_password_hash(password))
        session.add(user)
        session.commit()


def update_user(user):
    with Session() as session:
        session.add(user)
        session.commit()


def delete_user_by_id(user_id):
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()


def find_all_users():
    with Session() as session:
        users = session.query(User).all()
        return users


def find_by_email(email):
    with Session() as session:
        user = session.query(User).filter_by(email=email).first()
        return user


def find_user_by_id(id):
    with Session() as session:
        user = session.query(User).filter_by(id=id).first()
        return user


def check_password(password, email):
    user = find_by_email(email)
    if check_password_hash(user.password, password):
        return user
    else: -1


def change_password(password, email):
    user = find_by_email(email)
    user.password = generate_password_hash(password)
    with Session() as session:
        session.commit()