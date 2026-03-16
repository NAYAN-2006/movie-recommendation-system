from flask import Blueprint
from controllers.rating_controller import rate_movie
from middleware.auth_middleware import token_required

rating_bp = Blueprint("ratings", __name__)


@rating_bp.route("/rate", methods=["POST"])
@token_required()
def rate_movie_route():
  return rate_movie()

