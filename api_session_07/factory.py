from flask import Flask
from config import DefaultConfig
from errors import register_error_handlers
from extensions import db, migrate
from health import health_bp
from orders import orders_bp
from products import products_bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or DefaultConfig)
    app.json.ensure_ascii = False
    app.json.sort_keys = False
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)
    register_error_handlers(app)
    return app
