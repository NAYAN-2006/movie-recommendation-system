from flask import request, jsonify
from mysql.connector import Error
from config.db import get_connection


def add_watch_history():
  data = request.get_json() or {}
  user_id = data.get("user_id")
  movie_id = data.get("movie_id")

  if not all([user_id, movie_id]):
    return jsonify({"message": "user_id and movie_id are required"}), 400

  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      insert_query = """
        INSERT INTO watch_history (user_id, movie_id, watched_at)
        VALUES (%s, %s, NOW())
      """
      cursor.execute(insert_query, (user_id, movie_id))
      conn.commit()
    return jsonify({"message": "Watch history added"})
  except Error as e:
    print(f"Error in add_watch_history: {e}")
    conn.rollback()
    return jsonify({"message": "Failed to add watch history"}), 500
  finally:
    conn.close()


def get_watch_history(user_id):
  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      query = """
        SELECT
          m.movie_id,
          m.title,
          m.release_year,
          m.duration,
          m.language,
          wh.watched_at
        FROM watch_history wh
        JOIN movies m ON wh.movie_id = m.movie_id
        WHERE wh.user_id = %s
        ORDER BY wh.watched_at DESC;
      """
      cursor.execute(query, (user_id,))
      rows = cursor.fetchall()
    return jsonify(rows)
  except Error as e:
    print(f"Error in get_watch_history: {e}")
    return jsonify({"message": "Failed to fetch watch history"}), 500
  finally:
    conn.close()

