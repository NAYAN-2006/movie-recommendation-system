from flask import Blueprint
from controllers.watch_history_controller import add_watch_history, get_watch_history
from middleware.auth_middleware import token_required

watch_history_bp = Blueprint("watch_history", __name__)


@watch_history_bp.route("/watch-history", methods=["POST"])
@token_required()
def add_watch_history_route():
  return add_watch_history()


@watch_history_bp.route("/watch-history/<int:user_id>", methods=["GET"])
@token_required()
def get_watch_history_route(user_id):
  return get_watch_history(user_id)

