import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'

    # Elasticsearch Configuration
    ELASTICSEARCH_HOSTS = os.environ.get('ELASTICSEARCH_HOSTS') or '["http://localhost:9200"]' # JSON string for list
    ELASTICSEARCH_USER = os.environ.get('ELASTICSEARCH_USER') or None
    ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD') or None
