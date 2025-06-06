from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from .models import db  # Import db from models.py
from elasticsearch_dsl import connections
from elasticsearch import Elasticsearch
import json

# Initialize extensions
# db is already initialized in models.py, we just need to initialize it with the app
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Elasticsearch Connection Setup
    es_hosts_str = app.config.get('ELASTICSEARCH_HOSTS')
    es_user = app.config.get('ELASTICSEARCH_USER')
    es_password = app.config.get('ELASTICSEARCH_PASSWORD')

    es_hosts = None
    if isinstance(es_hosts_str, str):
        try:
            parsed_hosts = json.loads(es_hosts_str)
            if isinstance(parsed_hosts, list):
                es_hosts = parsed_hosts
            else: # If it's a single URL string not in a list
                es_hosts = [es_hosts_str]
        except json.JSONDecodeError:
            es_hosts = [h.strip() for h in es_hosts_str.split(',')]
    elif isinstance(es_hosts_str, list):
        es_hosts = es_hosts_str

    if es_hosts:
        http_auth = None
        if es_user and es_password:
            http_auth = (es_user, es_password)

        try:
            connections.create_connection(
                alias='default',
                hosts=es_hosts,
                http_auth=http_auth,
                timeout=20
            )
            app.elasticsearch = Elasticsearch(es_hosts, http_auth=http_auth, timeout=20)
            # Test connection
            if app.elasticsearch.ping():
                print(f"Successfully connected to Elasticsearch at {es_hosts}")
            else:
                print(f"Failed to ping Elasticsearch at {es_hosts}. Check connection and configuration.")
                app.elasticsearch = None # Set to None if ping fails
        except Exception as e:
            print(f"Error connecting to Elasticsearch at {es_hosts}: {e}")
            app.elasticsearch = None # Set to None if connection fails
    else:
        app.elasticsearch = None
        print("Elasticsearch hosts not configured or invalid.")

    # Register blueprints here
    from .routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Import models to ensure they are registered with SQLAlchemy
    # (though direct import in models.py by db object should be sufficient)
    from . import models

    return app
