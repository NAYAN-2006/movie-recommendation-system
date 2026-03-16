from flask import jsonify
from mysql.connector import Error
from config.db import get_connection


def get_recommendations(user_id):
  """Recommend movies based on genres of watched movies, excluding already watched ones."""
  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      query = """
        SELECT DISTINCT m.*
        FROM movies m
        JOIN movie_genres mg ON m.movie_id = mg.movie_id
        WHERE mg.genre_id IN (
          SELECT mg2.genre_id
          FROM watch_history wh
          JOIN movie_genres mg2 ON wh.movie_id = mg2.movie_id
          WHERE wh.user_id = %s
        )
        AND m.movie_id NOT IN (
          SELECT movie_id FROM watch_history WHERE user_id = %s
        )
        LIMIT 10;
      """
      cursor.execute(query, (user_id, user_id))
      rows = cursor.fetchall()
    return jsonify(rows)
  except Error as e:
    print(f"Error in get_recommendations: {e}")
    return jsonify({"message": "Failed to fetch recommendations"}), 500
  finally:
    conn.close()

