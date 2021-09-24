from models.serializer import Serializer
from flask_login import UserMixin
from main import db

class Usuario(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), unique=True)
	email = db.Column(db.String(200), unique=True)
	password = db.Column(db.String(32))
	rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
	@property
	def serialize(self):
		rol = Rol.query.filter_by(id=self.rol_id).first()
		return {
				'username': self.username,
				#'email': self.email,
				'rol': rol.tipo_rol
			}


class Rol(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tipo_rol = db.Column(db.String(40), unique=True)
	usuariorol = db.relationship('Usuario', backref='rol', lazy='dynamic')




@app.route('/usuarios', methods=['POST'])
def crear_usuario():
	try:
		datos_usuario = request.get_json()
		if Usuario.query.filter_by(username=datos_usuario['username']).first():
			return 'Ya existe usuario con ese nombre de usuario.', 200

		if Usuario.query.filter_by(email=datos_usuario['email']).first():
			return 'Ya existe usuario con ese email.', 200

		usuario = Usuario(username=datos_usuario['username'], email=datos_usuario['email'], password=datos_usuario['password'], rol_id = 2)
		db.session.add(usuario)
		db.session.commit()
		return 'Usuario creado satisfactoriamente.', 200
	except:
		return 'ERROR', 400



@app.route('/usuarios/<string:username>', methods=['GET'])
def ver_usuario(username):
	usuario = Usuario.query.filter_by(username=username).first()
	if not usuario:
		return "No existe el usuario", 404
	return jsonify([usuario.serialize]), 200