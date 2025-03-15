from .auth import auth_bp, register, login
from .user import user_bp, get_users, get_user, put_user, delete_user
from .location import location_bp, get_locations, get_location, put_location, delete_location, post_location
from .reaction import comment_bp, post_reaction