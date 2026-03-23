from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from models.user_model import find_user_by_email, create_user, find_user_by_id


def register():
  data = request.get_json() or {}
  print("Register request data:", data)
  name = (data.get("name") or "").strip()
  email = (data.get("email") or "").strip().lower()
  password = (data.get("password") or "").strip()

  if not all([name, email, password]):
    return jsonify({"message": "Name, email, and password are required"}), 400

  existing = find_user_by_email(email)
  print("Existing user check:", existing)
  if existing:
    return jsonify({"message": "Email already registered"}), 409

  password_hash = generate_password_hash(password)

  try:
    user_id = create_user(name, email, password_hash)
    print("User created with ID:", user_id)
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
  except Exception as e:
    print("Error creating user:", e)
    return jsonify({"message": "Failed to register user"}), 500


def login():
  data = request.get_json() or {}
  print("Login request data:", data)
  email = (data.get("email") or "").strip().lower()
  password = (data.get("password") or "").strip()

  if not all([email, password]):
    return jsonify({"message": "Email and password are required"}), 400

  user = find_user_by_email(email)
  print("User found:", user)
  if not user:
    return jsonify({"message": "User not found"}), 404

  stored_password_raw = user.get("password", "")

  try:
    ok = check_password_hash(stored_password_raw, password)
  except ValueError:
    # Stored password isn't a werkzeug hash (likely plain text). If it matches, upgrade it.
    if stored_password_raw == password:
      # Re-hash the password for future logins.
      new_hash = generate_password_hash(password)
      from models.user_model import update_user_password

      try:
        user_id_temp = user.get("user_id") or user.get("id")
        update_user_password(user_id_temp, new_hash)
      except Exception:
        # Ignore failure to upgrade, proceed with login based on plaintext match.
        pass

      ok = True
    else:
      return jsonify({"message": "Invalid password"}), 401

  if not ok:
    return jsonify({"message": "Invalid password"}), 401

  # Get user_id - handle both 'id' and 'user_id' column names
  user_id = user.get("user_id") or user.get("id")
  
  payload = {
    "user_id": user_id,
    "email": user["email"],
    "is_admin": bool(user.get("is_admin", 0)),
    "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
  }

  token = jwt.encode(
    payload,
    current_app.config["JWT_SECRET_KEY"],
    algorithm=current_app.config["JWT_ALGORITHM"],
  )

  return jsonify(
    {
      "token": token,
      "user": {"id": user_id, "name": user["name"], "email": user["email"]},
    }
  ), 200


def get_profile():
  """Get current user profile (requires valid JWT token)."""
  token = request.headers.get("Authorization")
  if not token:
    return jsonify({"message": "Missing authorization token"}), 401

  try:
    # Remove 'Bearer ' prefix if present
    if token.startswith("Bearer "):
      token = token[7:]

    payload = jwt.decode(
      token,
      current_app.config["JWT_SECRET_KEY"],
      algorithms=[current_app.config["JWT_ALGORITHM"]],
    )
  except jwt.ExpiredSignatureError:
    return jsonify({"message": "Token expired"}), 401
  except jwt.InvalidTokenError:
    return jsonify({"message": "Invalid token"}), 401

  user_id = payload.get("user_id")
  if not user_id:
    return jsonify({"message": "Invalid token"}), 401

  user = find_user_by_id(user_id)
  if not user:
    return jsonify({"message": "User not found"}), 404

  return jsonify({"id": user.get("user_id"), "name": user["name"], "email": user["email"]})

