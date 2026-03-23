from typing import Optional, Dict, Any
from mysql.connector import Error
from config.db import get_connection


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
  # Normalize email lookup to be case-insensitive.
  query = "SELECT * FROM users WHERE LOWER(email) = LOWER(%s)"
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


def find_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
  """Find user by user_id."""
  query = "SELECT * FROM users WHERE user_id = %s"
  conn = get_connection()
  try:
    with conn.cursor(dictionary=True) as cursor:
      cursor.execute(query, (user_id,))
      return cursor.fetchone()
  except Error as e:
    print(f"Error in find_user_by_id: {e}")
    raise
  finally:
    conn.close()


def create_user(name: str, email: str, password_hash: str) -> int:
  """Insert new user into existing users table."""
  query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(query, (name, email, password_hash))
      conn.commit()
      return cursor.lastrowid
  except Error as e:
    print(f"Error in create_user: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()


def update_user_password(user_id: int, password_hash: str) -> None:
  """Update a user record with a new password hash."""
  query = "UPDATE users SET password = %s WHERE user_id = %s"
  conn = get_connection()
  try:
    with conn.cursor() as cursor:
      cursor.execute(query, (password_hash, user_id))
      conn.commit()
  except Error as e:
    print(f"Error in update_user_password: {e}")
    conn.rollback()
    raise
  finally:
    conn.close()

