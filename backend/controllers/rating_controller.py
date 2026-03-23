from flask import request, jsonify, g
from mysql.connector import Error
from config.db import get_connection


def rate_movie(movie_id: int = None):
  """
  Save/update a user's rating for a movie.

  Supports:
  - POST /movies/<movie_id>/rate with body: { "rating": 4 }
  - POST /rate with body: { "movie_id": 1, "rating_value": 4 } (legacy)
  """
  data = request.get_json() or {}
  user_id = getattr(g, "current_user", {}).get("user_id") or data.get("user_id")
  resolved_movie_id = movie_id or data.get("movie_id")
  rating_value = data.get("rating") if "rating" in data else data.get("rating_value")

  if not all([user_id, resolved_movie_id, rating_value]):
    return (
      jsonify({"message": "movie_id and rating are required"}),
      400,
    )

  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      select_query = (
        "SELECT rating_id FROM ratings WHERE user_id = %s AND movie_id = %s"
      )
      cursor.execute(select_query, (user_id, resolved_movie_id))
      existing = cursor.fetchone()

      if existing:
        update_query = "UPDATE ratings SET rating_value = %s WHERE rating_id = %s"
        cursor.execute(update_query, (rating_value, existing["rating_id"]))
      else:
        insert_query = """
          INSERT INTO ratings (user_id, movie_id, rating_value)
          VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, resolved_movie_id, rating_value))

      conn.commit()

    return jsonify({"message": "Rating saved successfully"})
  except Error as e:
    print(f"Error in rate_movie: {e}")
    conn.rollback()
    return jsonify({"message": "Failed to save rating"}), 500
  finally:
    conn.close()

