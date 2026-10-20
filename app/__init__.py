import os
from flask import Flask
from .config import config
from .database import db


def create_app(env=None):
    env = env or os.getenv("FLASK_ENV", "production")
    app = Flask(__name__)
    app.config.from_object(config.get(env, config["production"]))
    db.init_app(app)

    from .routes.clientes import bp as clientes_bp
    app.register_blueprint(clientes_bp)
    return app
