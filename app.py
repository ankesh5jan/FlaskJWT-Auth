from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'SUPER_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
#app.secret_key = 'secret_key'
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()  # Get JSON data from request body
        username = data['username']
        password = data['password']

        if not username or not password:
            return {'message': 'Please provide username and password.'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists.'}, 400

        new_user = User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully.'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200

        return {'message': 'Invalid username or password.'}, 401

class GetUser(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {'user_id': current_user_id}, 200


class UserList(Resource):
    def get(self):
        users = User.query.all()
        user_list = []

        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username
                # Don't include password for security reasons
            }
            user_list.append(user_data)

        return jsonify(users=user_list)


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(GetUser, '/getuser')
api.add_resource(UserList, '/')

if __name__ == '__main__':
    app.run (host="0.0.0.0", port=5000, debug=True)