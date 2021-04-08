from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import json
from datetime import date
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'iniciales.clqpka2rpvnz.us-west-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'iniciales'
app.config['MYSQL_PASSWORD'] = 'iniciales'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

@app.route('/registro', methods=['POST'])
def registro():

	if request.method == 'POST':

		try:

			identifier = request.json['identifier']
			names = request.json['names']
			surNames = request.json['surNames']
			email = request.json['email']
			photoUrl = request.json['photoUrl']
			password = request.json['password']

			cur = mysql.connection.cursor()
			cur.execute("""INSERT INTO Usuario (Registro_académico, Nombres, Apellidos, Correo_electrónico, Foto, Contraseña)
				VALUES(%s, %s, %s, %s, %s, %s)""",(identifier, names, surNames, email, photoUrl, password))

			mysql.connection.commit()

			return jsonify(
				{
					"success": "true",
					"msg": "Usuario registrado exitosamente"

				},
				{
					"identifier": identifier,
					"names": names,
					"surNames": surNames,
					"email": email,
					"photoUrl": photoUrl
				}
			)
				
		except:

			return jsonify(
				{
					"success": "false",
					"msg": "Usuario ya registrado"
				}
			)

@app.route('/perfil', methods=['GET'])
def perfil():

	identifier = request.args.get("identifier",None)

	try:
	
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM Usuario WHERE Registro_académico = {0}'.format(identifier))
		data = cur.fetchall()

		return jsonify(
			{
				"success": "true",
				"msg": "Información del Usuario"
			},
			{
				"identifier": data[0][0],
				"names": data[0][1],
				"surNames": data[0][2],
				"email": data[0][3],
				"photoUrl": data[0][4]
			}
		)
			

	except:

		return jsonify(
			{
				"success": "false",
				"msg": "Usuario no encontrado"
			}
		)

@app.route('/login', methods=['POST'])
def login():

	if request.method == 'POST':


		identifier = request.json['identifier']
		password = request.json['password']

		
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM Usuario WHERE Registro_académico = "{0}"'.format(identifier))
		data = cur.fetchall()

		if data[0][5] == password:

			return jsonify(
				{
					"success": "true",
					"msg": "Inicio Sesión: " + identifier
				}
			)
		
		return jsonify(
			{
					"success": "false",
					"msg": "Contraseña Incorrecta"
			}
		)


@app.route('/recuperar-cuenta', methods=['POST'])
def recuperar_cuenta():

	if request.method == 'POST':

		identifier = request.json['identifier']
		email = request.json['email']

		try:
			cur = mysql.connection.cursor()
			cur.execute('SELECT * FROM Usuario WHERE Registro_académico = {0}'.format(identifier))
			data = cur.fetchall()

			if data[0][3] == email:

				return jsonify(
					{
						"success": "true",
						"msg": "Se encontró el Usuario"
					},
					{
						"identifier": data[0][0],
						"names": data[0][1],
						"surNames": data[0][2],
						"email": data[0][3],
						"password": data[0][5]
					}
				)
		
			return jsonify(
				{
					"success": "false",
					"msg": "Email ingresado incorrectamente"
				}
			)

		except:

			return jsonify(
				{
					"success": "false",
					"msg": "Usuario no Encontrado"
				}
			)

@app.route('/modificar-usuario', methods=['POST'])
def modificar_usuario():
	
	if request.method == 'POST':

		try:

			identifier = request.json['identifier']
			names = request.json['names']
			surNames = request.json['surNames']
			email = request.json['email']
			photoUrl = request.json['photoUrl']
			password = request.json['password']

			cur = mysql.connection.cursor()
			cur.execute("""
				UPDATE Usuario
				SET Nombres = %s,
					Apellidos = %s,
					Correo_electrónico = %s,
					Foto = %s,
					Contraseña = %s
				WHERE Registro_académico = %s	
				""", (names, surNames, email, photoUrl, password, identifier))

			mysql.connection.commit()
			
			return jsonify(
				{
					"success": "true",
					"msg": "Actualizado el Usuario"
				},
				{
					"identifier": identifier,
					"names": names,
					"surNames": surNames,
					"email": email,
					"photoUrl": photoUrl
				}
			)
		

		except:
			return jsonify(
			{
				"success": "false",
				"msg": "Ocurrió un Error"
			}
		)	


@app.route('/listado-cursos', methods=['GET'])
def listado_cursos():

	try:

		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM Catedra')
		data = cur.fetchall()
		listaCursos = []

		for i in data:

			curso = {
				"registro": i[0],
				"código": i[1],
			}

			listaCursos.append(curso)

		return jsonify(
			{
				"success": "true",
				"msg": "Listado de Cursos en el Sistema"

			},
			listaCursos
		)

	except:

		return jsonify(
				{
					"success": "false",
					"msg": "Ocurrió un Error al envíar el listado de Cursos"
				}
			)
	
@app.route('/listado-catedraticos', methods=['GET'])
def listado_catedraticos():

	try:

		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM Catedrático')
		data = cur.fetchall()
		listaCatedraticos = []

		for i in data:

			catedratico = {
				"registro": i[0],
				"nombre": i[1],
			}

			listaCatedraticos.append(catedratico)

		return jsonify(
			{
				"success": "true",
				"msg": "Listado de Cursos en el Sistema"

			},
			listaCatedraticos
		)

	except:

		return jsonify(
				{
					"success": "false",
					"msg": "Ocurrió un Error al envíar el listado de Catedráticos"
				}
			)



@app.route('/', methods=['GET'])
def index():

	return "<H1>BACKEND PRACTICAS INICIALES: DESARROLLO WEB</H1>"

if __name__ == "__main__":
	app.run(threaded=True, port=5000,debug=True)	    