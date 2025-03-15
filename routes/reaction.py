from flask import request, abort, jsonify, Blueprint

from db_queries import create_reaction, get_all_reactions_in_location
from .dto import ReactionRequestInput
from .auth import login_required, current_user
from send_mail import send_email_on_new_review

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/reaction/<int:location_id>', methods=['POST'])
@login_required
def post_reaction(location_id):
    data = ReactionRequestInput(**request.json)
    if data.text is None and data.like is None:
        abort(400)

    create_reaction(current_user.id, location_id, data.text, data.like)
    send_email_on_new_review(location_id)
    reaction_json = {
        "text": data.text,
        "like": data.like,
        "location_id": location_id,
        "user_id": current_user.id
    }
    return jsonify(reaction_json), 200


@comment_bp.route('/reactions/<int:id>', methods=['GET'])
def get_reaction_for_location(id):
    reactions = get_all_reactions_in_location(id)
    if reactions is None:
        abort(404)
    else:
        locations_json = [
            {
                'comment_text': reaction.comment_text,
            } for reaction in reactions
        ]
        return jsonify(locations_json), 200