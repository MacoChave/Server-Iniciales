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

@app.route('/', methods=['GET'])
def index():

	return "<H1>BACKEND PRACTICAS INICIALES: DESARROLLO WEB</H1>"

if __name__ == "__main__":
	app.run(threaded=True, port=5000,debug=True)	    