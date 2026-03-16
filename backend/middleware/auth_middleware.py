from functools import wraps
from flask import request, jsonify, current_app, g
import jwt
from datetime import datetime, timezone


def token_required(admin_required: bool = False):
  """
  Protect routes with JWT.
  Expects header: Authorization: Bearer <token>.
  """

  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      auth_header = request.headers.get("Authorization", "")
      parts = auth_header.split()

      if len(parts) != 2 or parts[0].lower() != "bearer":
        return jsonify({"message": "Authorization header missing or invalid"}), 401

      token = parts[1]

      try:
        payload = jwt.decode(
          token,
          current_app.config["JWT_SECRET_KEY"],
          algorithms=[current_app.config["JWT_ALGORITHM"]],
        )

        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
          tz=timezone.utc
        ):
          return jsonify({"message": "Token has expired"}), 401

        g.current_user = {
          "user_id": payload.get("user_id"),
          "email": payload.get("email"),
          "is_admin": payload.get("is_admin", False),
        }

        if admin_required and not g.current_user["is_admin"]:
          return jsonify({"message": "Admin privileges required"}), 403

      except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

      return f(*args, **kwargs)

    return wrapper

  return decorator

