from flask import Flask, jsonify
from flask_mysqldb import MySQL


from config import config

app = Flask(__name__)
mysql = MySQL(app)


@app.route('/')
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


def pagina_not_found(error):
    return "<h1>La pagina que intentas buscar no existe...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_not_found)
    app.run(debug=True)


