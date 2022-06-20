from flask import Flask, jsonify, redirect, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin


from config import config

app = Flask(__name__)
CORS(app)
mysql = MySQL(app)



# Obtenemos los vuelos de la Base de datos
@cross_origin
@app.route('/', methods=['GET'])
def listar_vuelos():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT origen.aeropuerto_origen, origen.ciudad_orgien, destino.aeropuerto_destino, destino.ciudad_destino, compania.nombre_compania, compania.direccion, compania.telefono_compania, vuelo.modeloAvion, vuelo.capacidad, vuelo.numeroVuelo FROM `vuelo` INNER JOIN compania on vuelo._id_compania = compania._id_compania INNER JOIN itinerario on vuelo._id_itinerario = itinerario._id_itinerario INNER JOIN origen on itinerario._id_origen = origen._id_origen INNER JOIN destino on itinerario._id_destino = destino._id_destino"
        cursor.execute(sql)
        data = cursor.fetchall()

        vuelos = []

        for fila in data:
            vuelo = {"aeropuerto_origen": fila[0], "ciudad_orgien":fila[1], "aeropuerto_destino": fila[2], "ciudad_destino":fila[3], "nombre_compania":fila[4], "direccion_compnia":fila[5], "telefono_compania":fila[6], "modeloAvion": fila[7], "capacidad":fila[8], "numeroVuelo":fila[9]}
            vuelos.append(vuelo)
        return jsonify({"vuelos": vuelos, "mensaje":"Listado de vuelos"})
    except Exception as ex:
        return ex


# Login
@cross_origin
@app.route('/login', methods=['POST'])
def login():
    # if request.method == 'POST':
    try:
        cursor = mysql.connection.cursor()
        email = request.json['email']
        password = request.json['password']

        # Verificamos si existe el usuario
        is_exit = "SELECT * FROM `usuarios` WHERE usuarios.email = '{0}'" .format(email)
        cursor.execute(is_exit)
        user = cursor.fetchone()


        # Login
        if user != None:
            is_pass = check_password_hash(user[3], password)
            
            # Verificamos si la clave es correcta
            if is_pass:
                sql = "SELECT * FROM `usuarios` WHERE usuarios.email = '{0}'" .format(email)
                cursor.execute(sql)
                dato = cursor.fetchone()
                user = {"id": dato[0], "name": dato[1], "email":dato[2], "telefono":dato[4], "role":dato[5]}
                return jsonify({"user":user, "Mensaje": "Datos del usuaroio"})
            else:
                return "N"
        else:
            return jsonify({"no_found": "null", "Mensaje":"Lista de usutiop"})
    except Exception as ex:
        return ex



# Registrar usuario
@app.route('/registrar', methods=['POST'])
def registrar():
    cursor = mysql.connection.cursor()
    
    name = request.json['name']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])
    telefono = request.json['telefono']

    sql = "INSERT INTO `usuarios`(`name`, `email`, `password`, `telefono`) VALUES ('{0}','{1}','{2}','{3}')".format(name, email, password, telefono)
    cursor.execute(sql)
    mysql.connection.commit()
    return sql

# Mostramos una pantalla de 404
def pagina_not_found(error):
    return "<h1>La pagina que intentas buscar no existe...</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_not_found)
    app.run(debug=True)


