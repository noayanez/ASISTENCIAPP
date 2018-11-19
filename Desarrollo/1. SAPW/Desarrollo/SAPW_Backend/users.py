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
	'username' : fields.String,
	'password' : fields.String,
}

class UsersList(Resource):
	@marshal_with(user_fields, envelope='users')
	def get(self, **kwargs):
		#return Users.query.filter_by(id=1).first()
		print(Users.query.all())
		return Users.query.all()

	@marshal_with(user_fields, envelope='user')
	def post(self):
		args = parser.parse_args()
		new_user = Users(username=args['username'], password=args['password'])
		print(new_user)
		db.session.add(new_user)
		db.session.commit()
		return new_user, 201

api.add_resource(UsersList, '/users')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
