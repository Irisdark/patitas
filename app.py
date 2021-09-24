from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
import json
from sqlalchemy.inspection import inspect
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./ejemplo3.db'
app.config['SECRET_KEY'] = 'estaesunaclave1' 

# Creando la base (por las dudas)
try:
	print('Creando base...')
	db.create_all()
	print('Base creada!')
except:
	print('Ya existe la BD')

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

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



class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


class Mascota(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.Unicode(40))
	especie = db.Column(db.String(1), nullable=False)
	sexo = db.Column(db.String(1))
	color = db.Column(db.Unicode(60))
	edad = db.Column(db.String(1), nullable=False)
	tamanio = db.Column(db.String(1))
	oreja = db.Column(db.String(1))
	pelaje = db.Column(db.String(1))
	otra_informacion_mascota = db.Column(db.Unicode(240))
	departamento = db.Column(db.String(1), nullable=False)
	localidad = db.Column(db.Integer, nullable=False)
	calle = db.Column(db.Unicode(120))
	fecha_encuentro = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	mas_informacion_encuentro = db.Column(db.Unicode(240))
	nombre_contacto = db.Column(db.Unicode(100))
	celular_contacto = db.Column(db.Integer, nullable=False)
	telefono_contacto = db.Column(db.Integer)
	estado_mascota = db.Column(db.Integer, nullable=False)
	estado_publicacion = db.Column(db.Integer)
	fecha_publicacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
	@property
	def serialize(self):
		return {
				'id': self.id,
				'nombre': self.nombre,
				'especie': self.especie,
				'sexo': self.sexo,
				'color': self.color,
				'edad': self.edad,
				'tamanio': self.tamanio,
				'oreja': self.oreja,
				'pelaje': self.pelaje,
				'otra_informacion_mascota': self.otra_informacion_mascota,
				'departamento': self.departamento,
				'localidad': self.localidad,
				'calle': self.calle,
				'fecha_encuentro': self.fecha_encuentro,
				'mas_informacion_encuentro': self.mas_informacion_encuentro,
				'nombre_contacto': self.nombre_contacto,
				'celular_contacto': self.celular_contacto,
				'telefono_contacto': self.telefono_contacto,
				'estado_mascota': self.estado_mascota,
				'estado_publicacion': self.estado_publicacion,
				'fecha_publicacion': self.fecha_publicacion
			}


class Fotos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	img = db.Column(db.Text, unique=True, nullable=False)
	nombre = db.Column(db.Text, nullable=False)
	mimetype = db.Column(db.Text, nullable=False)


@app.route('/upload', methods=['POST'])
def subir_imagen():
	try:
		imagen = request.files['imagen']

		if not imagen:
			return 'No ha subido ninguna imagen', 400
		filename = secure_filename(imagen.filename)
		mimetype = imagen.mimetype

		img = Fotos(img=imagen.read(), mimetype=mimetype, nombre=filename)
		db.session.add(img)
		db.session.commit()

		return 'La imagen ha sido subida!'
	except:
		return 'ERROR', 400

@app.route('/imagen/<int:id>', methods=['GET'])
def mostrar_imagen(id):
	img = Fotos.query.filter_by(id=id).first()
	if not img:
		return "No existe la imagen", 404

	return Response(img.img, mimetype=img.mimetype)



@app.route('/mascotas', methods=['POST'])
def crear_mascota():
	try:
		datos_mascota = request.get_json()
		mascota = Mascota(
				nombre = datos_mascota['nombre'],
				especie = datos_mascota['especie'],
				sexo = datos_mascota['sexo'],
				color = datos_mascota['color'],
				edad = datos_mascota['edad'],
				tamanio = datos_mascota['tamanio'],
				oreja = datos_mascota['oreja'],
				pelaje = datos_mascota['pelaje'],
				otra_informacion_mascota = datos_mascota['otra_informacion_mascota'],
				departamento = datos_mascota['departamento'],
				localidad = datos_mascota['localidad'],
				calle = datos_mascota['calle'],
				mas_informacion_encuentro = datos_mascota['mas_informacion_encuentro'],
				nombre_contacto = datos_mascota['nombre_contacto'],
				celular_contacto = datos_mascota['celular_contacto'],
				telefono_contacto = datos_mascota['telefono_contacto'],
				estado_mascota = datos_mascota['estado_mascota'],
				estado_publicacion = 'P'
			)
		db.session.add(mascota)
		db.session.commit()
		return 'Mascota ingresada correctamente.', 200
	except:
		return 'ERROR', 400


@app.route('/mascotas', methods=['GET'])
def listar_mascota():
		lista_mascotas = Mascota.query.all()
		return jsonify([i.serialize for i in lista_mascotas]), 200



@login_manager.user_loader
def load_user(usuario_id):
	return Usuario.query.get(int(usuario_id))


@app.route('/login', methods=['POST'])
def index():
	datos_usuario = request.get_json()
	usuario = Usuario.query.filter_by(username=datos_usuario['username']).first()
	if usuario and usuario.password == datos_usuario['password']:
		login_user(usuario)
		return 'Ahora estás loggeado! :)'
	else:
		return 'Nombre de usuario o contraseña incorrecta.'


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return 'Ahora estás deslogueado :('


@app.route('/home')
@login_required
def home():
	return 'El usuario actual es: '+ current_user.username


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




if __name__ == '__main__':
	app.run(debug=True)