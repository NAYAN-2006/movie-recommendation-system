from flask import Flask
from flask_cors import CORS

from config.db import init_db_pool
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp
from routes.rating_routes import rating_bp
from routes.watch_history_routes import watch_history_bp
from routes.recommendation_routes import recommendation_bp


def create_app():
  app = Flask(__name__)

  # Simple JWT config (hard-coded). For production, move this to environment.
  app.config["JWT_SECRET_KEY"] = "your-very-secret-key"
  app.config["JWT_ALGORITHM"] = "HS256"

  # Initialise MySQL connection pool
  init_db_pool()

  # Allow React dev server to call this API
  CORS(
    app,
    origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
    max_age=3600,
  )

  # Register blueprints
  app.register_blueprint(auth_bp, url_prefix="/api")
  app.register_blueprint(movie_bp, url_prefix="/api")
  app.register_blueprint(rating_bp, url_prefix="/api")
  app.register_blueprint(watch_history_bp, url_prefix="/api")
  app.register_blueprint(recommendation_bp, url_prefix="/api")

  return app


if __name__ == "__main__":
  app = create_app()
  app.run(debug=True, port=5000)

