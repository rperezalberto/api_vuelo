from flask import Flask
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)
conexion = MySQL(app)

@app.route('/vuelos')
def listar_vuelos():
    # return ("Hola mundo")
    try:
       cursor = conexion.connection.cursor()
       cursor.execute(sql)
       datos = cursor.fetchall()
       return "datos"

    except Exception as ex:
        return ex


def pagina_not_found(error):
    return "<h1>La pagina que intentas buscar no existe...</h1>"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_not_found)
    app.run()

