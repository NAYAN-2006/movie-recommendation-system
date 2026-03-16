from flask import Blueprint
from controllers.recommendation_controller import get_recommendations
from middleware.auth_middleware import token_required

recommendation_bp = Blueprint("recommendations", __name__)


@recommendation_bp.route("/recommendations/<int:user_id>", methods=["GET"])
@token_required()
def recommendations_route(user_id):
  return get_recommendations(user_id)

