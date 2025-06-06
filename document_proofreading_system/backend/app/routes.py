from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from .models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from elasticsearch import ElasticsearchException

bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)

auth_api = Api(bp)
app_api = Api(api_bp)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 400

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return {'message': f'Hello {user.username}! This is a protected endpoint.'}, 200

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

class ElasticsearchStatus(Resource):
    def get(self):
        if not hasattr(current_app, 'elasticsearch') or current_app.elasticsearch is None:
            return {'status': 'error', 'message': 'Elasticsearch not configured or connection failed on startup'}, 500
        try:
            if current_app.elasticsearch.ping():
                info = current_app.elasticsearch.info()
                return {
                    'status': 'connected',
                    'cluster_name': info.get('cluster_name'),
                    'version': info.get('version', {}).get('number')
                }
            else:
                return {'status': 'error', 'message': 'Elasticsearch ping failed'}, 500
        except ElasticsearchException as e: # Catch specific Elasticsearch exceptions
            # current_app.logger.error(f"Elasticsearch connection error: {e}")
            return {'status': 'error', 'message': str(e.error), 'info': e.info}, 500
        except Exception as e: # Catch any other exceptions
            # current_app.logger.error(f"Unexpected error checking Elasticsearch status: {e}")
            return {'status': 'error', 'message': f"An unexpected error occurred: {str(e)}"}, 500

auth_api.add_resource(UserRegistration, '/register')
auth_api.add_resource(UserLogin, '/login')
auth_api.add_resource(ProtectedResource, '/protected') # This will be /auth/protected

app_api.add_resource(HelloWorld, '/hello') # This will be /api/hello
app_api.add_resource(ElasticsearchStatus, '/es-status') # New endpoint
