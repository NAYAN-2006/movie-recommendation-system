from flask import request, jsonify
from mysql.connector import Error
from config.db import get_connection


def rate_movie():
  data = request.get_json() or {}
  user_id = data.get("user_id")
  movie_id = data.get("movie_id")
  rating_value = data.get("rating_value")

  if not all([user_id, movie_id, rating_value]):
    return jsonify({"message": "user_id, movie_id, and rating_value are required"}), 400

  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      select_query = "SELECT id FROM ratings WHERE user_id = %s AND movie_id = %s"
      cursor.execute(select_query, (user_id, movie_id))
      existing = cursor.fetchone()

      if existing:
        update_query = "UPDATE ratings SET rating_value = %s WHERE id = %s"
        cursor.execute(update_query, (rating_value, existing["id"]))
      else:
        insert_query = """
          INSERT INTO ratings (user_id, movie_id, rating_value)
          VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, movie_id, rating_value))

      conn.commit()

    return jsonify({"message": "Rating saved successfully"})
  except Error as e:
    print(f"Error in rate_movie: {e}")
    conn.rollback()
    return jsonify({"message": "Failed to save rating"}), 500
  finally:
    conn.close()

