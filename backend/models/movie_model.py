from typing import List, Dict, Any, Optional, Tuple
from mysql.connector import Error
from config.db import get_connection


def list_genres() -> List[str]:
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute("SELECT genre_name FROM genres ORDER BY genre_name")
      return [row[0] for row in cursor.fetchall() if row and row[0]]
  except Error as e:
    print(f"Error in list_genres: {e}")
    raise
  finally:
    conn.close()


def get_movies(search: Optional[str] = None, genre: Optional[str] = None) -> List[Dict[str, Any]]:
  """
  Return movies including director, genres, poster_url, and average rating.

  Optional filters:
  - search: title contains
  - genre: exact genre_name
  """
  where = []
  params: List[Any] = []

  if search:
    where.append("m.title LIKE %s")
    params.append(f"%{search}%")

  if genre:
    where.append("g.genre_name = %s")
    params.append(genre)

  where_sql = f"WHERE {' AND '.join(where)}" if where else ""

  query = f"""
    SELECT
      m.movie_id,
      m.title,
      m.release_year,
      m.duration,
      m.language,
      m.director_id,
      d.director_name AS director_name,
      m.poster_url,
      m.backdrop_url,
      m.popularity,
      m.is_oscar_winner,
      m.country,
      COALESCE(AVG(r.rating_value), NULL) AS average_rating,
      COUNT(r.rating_id) AS rating_count,
      GROUP_CONCAT(DISTINCT g.genre_name ORDER BY g.genre_name SEPARATOR '||') AS genres
    FROM movies m
    LEFT JOIN directors d ON m.director_id = d.director_id
    LEFT JOIN movie_genres mg ON mg.movie_id = m.movie_id
    LEFT JOIN genres g ON g.genre_id = mg.genre_id
    LEFT JOIN ratings r ON r.movie_id = m.movie_id
    {where_sql}
    GROUP BY
      m.movie_id, m.title, m.release_year, m.duration, m.language, m.director_id,
      d.director_name, m.poster_url, m.backdrop_url, m.popularity, m.is_oscar_winner, m.country
    ORDER BY m.title;
  """

  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(query, tuple(params))
      rows = cursor.fetchall()
      for row in rows:
        raw = row.get("genres")
        row["genres"] = raw.split("||") if raw else []
        if row.get("average_rating") is not None:
          row["average_rating"] = float(row["average_rating"])
      return rows
  except Error as e:
    print(f"Error in get_movies: {e}")
    raise
  finally:
    conn.close()


def search_movies_by_title(keyword: str) -> List[Dict[str, Any]]:
  query = """
    SELECT
      m.movie_id,
      m.title,
      m.release_year,
      m.duration,
      m.language,
      d.director_name AS director_name
    FROM movies m
    LEFT JOIN directors d ON m.director_id = d.director_id
    WHERE m.title LIKE %s
    ORDER BY m.title;
  """
  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(query, (f"%{keyword}%",))
      return cursor.fetchall()
  except Error as e:
    print(f"Error in search_movies_by_title: {e}")
    raise
  finally:
    conn.close()


def get_movie_details(movie_id: int) -> Optional[Dict[str, Any]]:
  """Return movie details including director, actors, genres, and average rating."""
  conn = get_connection()
  try:
    result: Dict[str, Any] = {}

    movie_query = """
      SELECT
        m.movie_id,
        m.title,
        m.description,
        m.full_description,
        m.release_year,
        m.duration,
        m.language,
        m.director_id,
        d.director_name AS director_name
      FROM movies m
      LEFT JOIN directors d ON m.director_id = d.director_id
      WHERE m.movie_id = %s;
    """
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(movie_query, (movie_id,))
      movie = cursor.fetchone()
      if not movie:
        return None
      result["movie"] = movie

    actors_query = """
      SELECT a.actor_id, a.actor_name
      FROM movie_actors ma
      JOIN actors a ON ma.actor_id = a.actor_id
      WHERE ma.movie_id = %s;
    """
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(actors_query, (movie_id,))
      result["actors"] = cursor.fetchall()

    genres_query = """
      SELECT g.genre_id, g.genre_name
      FROM movie_genres mg
      JOIN genres g ON mg.genre_id = g.genre_id
      WHERE mg.movie_id = %s;
    """
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(genres_query, (movie_id,))
      result["genres"] = cursor.fetchall()

    avg_rating_query = """
      SELECT AVG(rating_value) AS avg_rating, COUNT(*) AS rating_count
      FROM ratings
      WHERE movie_id = %s;
    """
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(avg_rating_query, (movie_id,))
      rating_row = cursor.fetchone()
      result["average_rating"] = (
        float(rating_row["avg_rating"]) if rating_row["avg_rating"] is not None else None
      )
      result["rating_count"] = rating_row["rating_count"]

    return result
  except Error as e:
    print(f"Error in get_movie_details: {e}")
    raise
  finally:
    conn.close()


def admin_add_movie(movie_data: Dict[str, Any]) -> int:
  """Insert a new movie (admin)."""
  query = """
    INSERT INTO movies (title, description, release_year, duration, language, director_id)
    VALUES (%s, %s, %s, %s, %s, %s)
  """
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(
        query,
        (
          movie_data.get("title"),
          movie_data.get("description"),
          movie_data.get("release_year"),
          movie_data.get("duration"),
          movie_data.get("language"),
          movie_data.get("director_id"),
        ),
      )
      conn.commit()
      return cursor.lastrowid
  except Error as e:
    print(f"Error in admin_add_movie: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()


def admin_update_movie(movie_id: int, movie_data: Dict[str, Any]) -> bool:
  query = """
    UPDATE movies
    SET title = %s,
        description = %s,
        release_year = %s,
        duration = %s,
        language = %s,
        director_id = %s
    WHERE movie_id = %s
  """
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(
        query,
        (
          movie_data.get("title"),
          movie_data.get("description"),
          movie_data.get("release_year"),
          movie_data.get("duration"),
          movie_data.get("language"),
          movie_data.get("director_id"),
          movie_id,
        ),
      )
      conn.commit()
      return cursor.rowcount > 0
  except Error as e:
    print(f"Error in admin_update_movie: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()


def admin_delete_movie(movie_id: int) -> bool:
  query = "DELETE FROM movies WHERE movie_id = %s"
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(query, (movie_id,))
      conn.commit()
      return cursor.rowcount > 0
  except Error as e:
    print(f"Error in admin_delete_movie: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()

