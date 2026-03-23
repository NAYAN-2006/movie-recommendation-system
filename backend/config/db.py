from mysql.connector import pooling, Error

# Hardcoded MySQL credentials
host = "localhost"
user = "root"
password = "root"
database = "movie_recommendation"

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
      host=host,
      user=user,
      password=password,
      database=database,
    )
    print("MySQL connection pool initialised.")
  except Error as e:
    print(f"Error initialising MySQL connection pool: {e}")
    print(
      "Check your MySQL credentials."
    )
    raise


def get_connection():
  """Get a connection from the pool. Caller must close it."""
  if _connection_pool is None:
    raise RuntimeError("Connection pool not initialised. Call init_db_pool() first.")
  return _connection_pool.get_connection()

