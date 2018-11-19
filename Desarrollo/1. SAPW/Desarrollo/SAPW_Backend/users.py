from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, fields, marshal_with

import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')


user_fields = {
	'id' : fields.Integer,
	'username' : fields.String,
	'password' : fields.String,
}


class User(Resource):
	@marshal_with(user_fields, envelope='user')
	def get(self, idUser):
		user = Users.query.filter_by(id=idUser).first()
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
api.add_resource(User, '/users/<idUser>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
