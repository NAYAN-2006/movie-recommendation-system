from flask import Blueprint
from controllers.movie_controller import (
  get_movies,
  get_movie,
  search_movies,
  admin_create_movie,
  admin_update_movie_controller,
  admin_delete_movie_controller,
)
from middleware.auth_middleware import token_required

movie_bp = Blueprint("movies", __name__)


@movie_bp.route("/movies", methods=["GET"])
def get_movies_route():
  return get_movies()


@movie_bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie_route(movie_id):
  return get_movie(movie_id)


@movie_bp.route("/movies/search", methods=["GET"])
def search_movies_route():
  return search_movies()


@movie_bp.route("/admin/movies", methods=["POST"])
@token_required(admin_required=True)
def admin_add_movie_route():
  return admin_create_movie()


@movie_bp.route("/admin/movies/<int:movie_id>", methods=["PUT"])
@token_required(admin_required=True)
def admin_update_movie_route(movie_id):
  return admin_update_movie_controller(movie_id)


@movie_bp.route("/admin/movies/<int:movie_id>", methods=["DELETE"])
@token_required(admin_required=True)
def admin_delete_movie_route(movie_id):
  return admin_delete_movie_controller(movie_id)

