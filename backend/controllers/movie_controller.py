from flask import request, jsonify
from models.movie_model import (
  get_movies as query_movies,
  list_genres,
  get_movie_details,
  search_movies_by_title,
  admin_add_movie,
  admin_update_movie,
  admin_delete_movie,
)


def get_movies():
  try:
    search = request.args.get("search", "").strip() or None
    genre = request.args.get("genre", "").strip() or None
    movies = query_movies(search=search, genre=genre)
    genres = list_genres()
    return jsonify({"movies": movies, "genres": genres})
  except Exception:
    return jsonify({"message": "Failed to fetch movies"}), 500


def get_movie(movie_id):
  try:
    details = get_movie_details(movie_id)
    if not details:
      return jsonify({"message": "Movie not found"}), 404
    movie = details.get("movie") or {}
    actors = details.get("actors") or []
    genres = details.get("genres") or []

    long_description = movie.get("full_description") or None
    short_description = movie.get("description") or None

    response = {
      "movieId": movie.get("movie_id"),
      "title": movie.get("title"),
      "description": short_description,
      "longDescription": long_description,
      "releaseYear": movie.get("release_year"),
      "duration": movie.get("duration"),
      "language": movie.get("language"),
      "director": movie.get("director_name"),
      "actors": [a.get("actor_name") for a in actors if a.get("actor_name")],
      "genre": [g.get("genre_name") for g in genres if g.get("genre_name")],
      "rating": details.get("average_rating"),
      "ratingCount": details.get("rating_count"),
      # Optional fields that the frontend may show if present later:
      "posterUrl": movie.get("poster_url") if isinstance(movie, dict) else None,
    }

    return jsonify(response)
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


def get_movie_categories():
  """
  Convenience endpoint for home-page sections.
  """
  try:
    movies = query_movies()

    def avg(m):
      return m.get("average_rating") if m.get("average_rating") is not None else 0.0

    trending = sorted(
      movies,
      key=lambda m: (m.get("popularity") or 0, avg(m), m.get("release_year") or 0),
      reverse=True,
    )[:12]

    top_rated = sorted(movies, key=lambda m: (avg(m), m.get("rating_count") or 0), reverse=True)[:12]
    new_releases = sorted(movies, key=lambda m: (m.get("release_year") or 0), reverse=True)[:12]
    oscar_winners = [m for m in movies if (m.get("is_oscar_winner") or 0) == 1][:12]
    indian = [m for m in movies if (m.get("country") or "").lower() == "india"][:12]
    international = [m for m in movies if (m.get("country") or "").lower() not in ("", "india")][:12]

    by_genre = {}
    for m in movies:
      for g in m.get("genres") or []:
        by_genre.setdefault(g, [])
        if len(by_genre[g]) < 12:
          by_genre[g].append(m)

    return jsonify(
      {
        "trending": trending,
        "topRated": top_rated,
        "newReleases": new_releases,
        "oscarWinners": oscar_winners,
        "indian": indian,
        "international": international,
        "byGenre": by_genre,
      }
    )
  except Exception:
    return jsonify({"message": "Failed to fetch categories"}), 500

