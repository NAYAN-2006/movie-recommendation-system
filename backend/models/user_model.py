from typing import Optional, Dict, Any
from mysql.connector import Error
from config.db import get_connection


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
  query = "SELECT * FROM users WHERE email = %s"
  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(query, (email,))
      return cursor.fetchone()
  except Error as e:
    print(f"Error in find_user_by_email: {e}")
    raise
  finally:
    conn.close()


def create_user(name: str, email: str, password_hash: str, is_admin: bool = False) -> int:
  """Insert new user into existing users table."""
  query = "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s)"
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(query, (name, email, password_hash, int(is_admin)))
      conn.commit()
      return cursor.lastrowid
  except Error as e:
    print(f"Error in create_user: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()

