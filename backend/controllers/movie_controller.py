from flask import request, jsonify
from models.movie_model import (
  get_all_movies,
  get_movie_details,
  search_movies_by_title,
  admin_add_movie,
  admin_update_movie,
  admin_delete_movie,
)


def get_movies():
  try:
    movies = get_all_movies()
    return jsonify(movies)
  except Exception:
    return jsonify({"message": "Failed to fetch movies"}), 500


def get_movie(movie_id):
  try:
    details = get_movie_details(movie_id)
    if not details:
      return jsonify({"message": "Movie not found"}), 404
    return jsonify(details)
  except Exception:
    return jsonify({"message": "Failed to fetch movie details"}), 500


def search_movies():
  q = request.args.get("q", "").strip()
  if not q:
    return jsonify([])
  try:
    results = search_movies_by_title(q)
    return jsonify(results)
  except Exception:
    return jsonify({"message": "Failed to search movies"}), 500


def admin_create_movie():
  data = request.get_json() or {}
  if not data.get("title"):
    return jsonify({"message": "Title is required"}), 400
  try:
    movie_id = admin_add_movie(data)
    return jsonify({"message": "Movie created", "movie_id": movie_id}), 201
  except Exception:
    return jsonify({"message": "Failed to create movie"}), 500


def admin_update_movie_controller(movie_id):
  data = request.get_json() or {}
  try:
    updated = admin_update_movie(movie_id, data)
    if not updated:
      return jsonify({"message": "Movie not found"}), 404
    return jsonify({"message": "Movie updated"})
  except Exception:
    return jsonify({"message": "Failed to update movie"}), 500


def admin_delete_movie_controller(movie_id):
  try:
    deleted = admin_delete_movie(movie_id)
    if not deleted:
      return jsonify({"message": "Movie not found"}), 404
    return jsonify({"message": "Movie deleted"})
  except Exception:
    return jsonify({"message": "Failed to delete movie"}), 500

