from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

from models.user_model import find_user_by_email, create_user


def register():
  data = request.get_json() or {}
  name = data.get("name")
  email = data.get("email")
  password = data.get("password")

  if not all([name, email, password]):
    return jsonify({"message": "Name, email, and password are required"}), 400

  existing = find_user_by_email(email)
  if existing:
    return jsonify({"message": "Email already registered"}), 409

  password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

  try:
    user_id = create_user(name, email, password_hash, is_admin=False)
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
  except Exception:
    return jsonify({"message": "Failed to register user"}), 500


def login():
  data = request.get_json() or {}
  email = data.get("email")
  password = data.get("password")

  if not all([email, password]):
    return jsonify({"message": "Email and password are required"}), 400

  user = find_user_by_email(email)
  if not user:
    return jsonify({"message": "Invalid credentials"}), 401

  stored_hash = user.get("password", "").encode("utf-8")
  if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
    return jsonify({"message": "Invalid credentials"}), 401

  payload = {
    "user_id": user["id"],
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
      "user": {"id": user["id"], "name": user["name"], "email": user["email"]},
    }
  )

