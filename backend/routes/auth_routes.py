from flask import Blueprint
from controllers.auth_controller import register, login, get_profile

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_route():
  return register()


@auth_bp.route("/login", methods=["POST"])
def login_route():
  return login()


@auth_bp.route("/users/profile", methods=["GET"])
def profile_route():
  return get_profile()

