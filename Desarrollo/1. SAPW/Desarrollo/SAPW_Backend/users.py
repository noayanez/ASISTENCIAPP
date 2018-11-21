from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, fields, marshal_with
from datetime import datetime
import os
from flask_cors import CORS

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)


class Usuariotrabajador(db.Model):
	__tablename__ = 'trabajador'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(45), nullable=False)
	dni = db.Column(db.String(8), unique=True, nullable=False)
	salario = db.Column(db.String(4), nullable=False)
	telefono = db.Column(db.String(9), nullable=False)
	correo = db.Column(db.String(45), unique=True, nullable=False)
	usuario = db.Column(db.String(45), unique=True, nullable=False)
	password = db.Column(db.String(45), nullable=False)
	historialasistencia = db.relationship('Historialasistencia', backref='UsuarioTrabajador', lazy=True)

class Historialasistencia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	horallegada = db.Column(db.DateTime, nullable=False)
	minutostardanza = db.Column(db.Integer, nullable=False)
	usuariotrabajador_id = db.Column(db.Integer, db.ForeignKey('trabajador.id'))
	

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')


parserUsuarioTrabajador = reqparse.RequestParser()
parserUsuarioTrabajador.add_argument('nombre')
parserUsuarioTrabajador.add_argument('dni')
parserUsuarioTrabajador.add_argument('salario')
parserUsuarioTrabajador.add_argument('telefono')
parserUsuarioTrabajador.add_argument('correo')
parserUsuarioTrabajador.add_argument('usuario')
parserUsuarioTrabajador.add_argument('password')

parserHistorialAsistencia = reqparse.RequestParser()
parserHistorialAsistencia.add_argument('dni')


user_fields = {
	'id' : fields.Integer,
	'username' : fields.String,
	'password' : fields.String,
}

usuariotrabajador_fields = {
	'id' : fields.Integer,
	'nombre' : fields.String,
	'dni' : fields.String,
	'salario' : fields.String,
	'telefono' : fields.String,
	'correo' : fields.String,
	'usuario' : fields.String,
	'password' : fields.String,
}


class UsuarioTrabajador(Resource):
	@marshal_with(usuariotrabajador_fields, envelope='UsuarioTrabajador')
	def get(self, dni):
		usuariotrabajador = Usuariotrabajador.query.filter_by(dni=dni).first()
		return usuariotrabajador

class UsuarioTrabajadorList(Resource):
	@marshal_with(usuariotrabajador_fields, envelope='UsuariosTrabajadores')
	def get(self, **kwargs):
		return Usuariotrabajador.query.all()

	@marshal_with(usuariotrabajador_fields, envelope='UsuarioTrabajador')
	def post(self):
		args = parserUsuarioTrabajador.parse_args()
		print(args)
		new_usuariotrabajador = Usuariotrabajador(nombre=args['nombre'], dni=args['dni'], salario=args['salario'], telefono=args['telefono'], correo=args['correo'], usuario=args['usuario'], password=args['password'])
		db.session.add(new_usuariotrabajador)
		db.session.commit()
		return new_usuariotrabajador, 201


class HistorialAsistencia(Resource):
	def post(self):
		args = parserHistorialAsistencia.parse_args()
		usuariotrabajador = Usuariotrabajador.query.filter_by(dni=args['dni']).first()
		print(usuariotrabajador)
		horallegada = datetime.now()
		tardanza = MinutosdeTardanza(horallegada)
		historialasistencia = Historialasistencia(horallegada=horallegada, minutostardanza=tardanza, usuariotrabajador_id=usuariotrabajador.id)
		print(historialasistencia)
		db.session.add(historialasistencia)
		db.session.commit()
		return tardanza, 200

# APIS CON FORMATO DE GUIA

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

#Funciones adicionales

def MinutosdeTardanza(llegada):
	horallegada = datetime.now()
	horaentrada = horallegada.replace(hour=9, minute=0, second=0)
	diferencia = horallegada - horaentrada

	days, seconds = diferencia.days, diferencia.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60

	if horallegada > horaentrada:
		#print("El empleado llego: " + str(hours) +" hora(s) " + "y " + str(minutes) + " minuto(s) tarde")
		return (hours*60 + minutes)
	else:
		return 0



api.add_resource(UsersList, '/users')
api.add_resource(User, '/users/<idUser>')
api.add_resource(Login, '/users/login/<username>/<password>')


api.add_resource(UsuarioTrabajadorList, '/usuariotrabajador')
api.add_resource(UsuarioTrabajador, '/usuariotrabajador/<dni>')
api.add_resource(HistorialAsistencia, '/asistencia')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
