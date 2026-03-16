import os
from mysql.connector import pooling, Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("root", "root")
DB_NAME = os.getenv("DB_NAME", "movie_recommendation")

_connection_pool = None


def init_db_pool():
  """Initialise global MySQL connection pool."""
  global _connection_pool
  if _connection_pool is not None:
    return

  try:
    _connection_pool = pooling.MySQLConnectionPool(
      pool_name="movie_pool",
      pool_size=10,
      pool_reset_session=True,
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASSWORD,
      database=DB_NAME,
    )
    print("MySQL connection pool initialised.")
  except Error as e:
    print(f"Error initialising MySQL connection pool: {e}")
    print(
      "Check your MySQL credentials. Set DB_HOST/DB_USER/DB_PASSWORD/DB_NAME in backend/.env "
      "(copy from backend/.env.example)."
    )
    raise


def get_connection():
  """Get a connection from the pool. Caller must close it."""
  if _connection_pool is None:
    raise RuntimeError("Connection pool not initialised. Call init_db_pool() first.")
  return _connection_pool.get_connection()

