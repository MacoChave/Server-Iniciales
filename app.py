from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '441320'
app.config['MYSQL_DB'] = 'cursos_ingenieria'

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
			cur.execute('INSERT INTO usuarios (identifier, names, surNames, email, photoUrl, password) VALUES(%s, %s, %s, %s, %s, %s)',
			(identifier, names, surNames, email, photoUrl, password))

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
		cur.execute('SELECT * FROM usuarios WHERE identifier = {0}'.format(identifier))
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

@app.route('/login', methods=['GET'])
def login():

	identifier = request.json['identifier']
	password = request.json['password']

	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM usuarios WHERE identifier = {0}'.format(identifier))
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

	except:

		return jsonify(
			{
				"success": "false",
				"msg": "Usuario no Encontrado"
			}
		)

@app.route('/recuperar-cuenta', methods=['GET'])
def recuperar_cuenta():

	identifier = request.json['identifier']
	email = request.json['email']

	try:
		cur = mysql.connection.cursor()
		cur.execute('SELECT * FROM usuarios WHERE identifier = {0}'.format(identifier))
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
				UPDATE usuarios
				SET names = %s,
					surNames = %s,
					email = %s,
					photoUrl = %s,
					password = %s
				WHERE identifier = %s	
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



@app.route('/', methods=['GET'])
def index():

	return "<H1>BACKEND PRACTICAS INICIALES: DESARROLLO WEB</H1>"

if __name__ == "__main__":
	app.run(threaded=True, port=5000,debug=True)	    