# app.py
from flask import Flask
from flask_bcrypt import Bcrypt
from flask.config import DevelopmentConfig, TestingConfig, ProductionConfig, LocalConfig
from .routes import register_routes

Bcrypt = Bcrypt()

config_options = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "local": LocalConfig
}

def create_app(config_name="development"):
    app = Flask(__name__)
    
    app.config.from_object(config_options.get(config_name, DevelopmentConfig))
    
    bcrypt.init_app(app)
    
    with app.app_context():
        register_routes(app)
    
    return app





    