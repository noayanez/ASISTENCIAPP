from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse, abort
from app import db, api
from app.models.users import Users

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

user_fields = {
	'id' : fields.Integer,
	'username' : fields.String,
	'password' : fields.String,
}

class Login(Resource):
	@marshal_with(user_fields, envelope='user')
	def get(self, username, password):
		print(username)
		user = Users.query.filter_by(username=username, password=password).first()
		return user

class User(Resource):
	@marshal_with(user_fields, envelope='user')
	def get(self, idUser):
		user = Users.query.filter_by(id=idUser).first()
		print(user)
		return user

	def delete(self, idUser):
		user = Users.query.filter_by(id=idUser).first()
		db.session.delete(user)
		db.session.commit()
		return '', 204

	@marshal_with(user_fields, envelope='user')
	def put(self, idUser):
		args = parser.parse_args()
		user = Users.query.filter_by(id=idUser).first()
		if args['username'] != None:
			user.username = args['username']
		
		if args['password'] != None:
			user.password = args['password']
		
		db.session.add(user)
		db.session.commit()
		return user, 201

class UsersList(Resource):
	@marshal_with(user_fields, envelope='users')
	def get(self, **kwargs):
		return Users.query.all()

	@marshal_with(user_fields, envelope='user')
	def post(self):
		args = parser.parse_args()
		new_user = Users(username=args['username'], password=args['password'])
		db.session.add(new_user)
		db.session.commit()
		return new_user, 201

api.add_resource(UsersList, '/users')
api.add_resource(User, '/users/<int:idUser>')
api.add_resource(Login, '/users/login/<username>/<password>')