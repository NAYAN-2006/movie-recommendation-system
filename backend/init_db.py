from mysql.connector import Error

from config.db import get_connection, init_db_pool


def _column_exists(cursor, table: str, column: str) -> bool:
  cursor.execute(
    """
    SELECT 1
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = %s
      AND COLUMN_NAME = %s
    LIMIT 1
    """,
    (table, column),
  )
  return cursor.fetchone() is not None


def migrate():
  init_db_pool()
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      if not _column_exists(cursor, "movies", "full_description"):
        cursor.execute("ALTER TABLE movies ADD COLUMN full_description LONGTEXT NULL")
        conn.commit()
        print("Added movies.full_description")
      else:
        print("movies.full_description already exists")

      if not _column_exists(cursor, "movies", "poster_url"):
        cursor.execute("ALTER TABLE movies ADD COLUMN poster_url TEXT NULL")
        conn.commit()
        print("Added movies.poster_url")
      else:
        print("movies.poster_url already exists")

      if not _column_exists(cursor, "movies", "backdrop_url"):
        cursor.execute("ALTER TABLE movies ADD COLUMN backdrop_url TEXT NULL")
        conn.commit()
        print("Added movies.backdrop_url")
      else:
        print("movies.backdrop_url already exists")

      if not _column_exists(cursor, "movies", "popularity"):
        cursor.execute("ALTER TABLE movies ADD COLUMN popularity INT NULL")
        conn.commit()
        print("Added movies.popularity")
      else:
        print("movies.popularity already exists")

      if not _column_exists(cursor, "movies", "is_oscar_winner"):
        cursor.execute(
          "ALTER TABLE movies ADD COLUMN is_oscar_winner TINYINT(1) NOT NULL DEFAULT 0"
        )
        conn.commit()
        print("Added movies.is_oscar_winner")
      else:
        print("movies.is_oscar_winner already exists")

      if not _column_exists(cursor, "movies", "country"):
        cursor.execute("ALTER TABLE movies ADD COLUMN country VARCHAR(60) NULL")
        conn.commit()
        print("Added movies.country")
      else:
        print("movies.country already exists")

      # Optional: if full_description is empty, seed it from description
      cursor.execute(
        """
        UPDATE movies
        SET full_description = description
        WHERE full_description IS NULL OR full_description = ''
        """
      )
      conn.commit()
      print("Seeded full_description from description where missing")
  except Error as e:
    conn.rollback()
    raise
  finally:
    conn.close()


if __name__ == "__main__":
  migrate()

