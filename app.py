from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import psycopg2  # Asegúrate de haber instalado esta librería
import mysql.connector

# Inicializar la aplicación
app = Flask(__name__)
CORS(app)
# Configuración de la base de datos


def get_db_connection():
    conn = mysql.connector.connect(
        host='bithey6ubcu8kcihev1e-mysql.services.clever-cloud.com',
        user='uakeyenhcaalsi1w',
        password='NfnTn35YPwpo08FaM4Dd',
        database='bithey6ubcu8kcihev1e',
        port=3306  # Cambia al puerto correcto si es diferente
    )
    return conn



# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def handle_form():
    data = request.get_json()  # Obtén los datos del formulario
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios!'}), 400

    # Inserta el usuario en la base de datos
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('INSERT INTO Users (User, Email, Password) VALUES (%s, %s, %s)', 
                    (username, email, password))
        conn.commit()  # Guarda los cambios
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500  # Devuelve un error si falla la inserción
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Usuario agregado exitosamente!'}), 201  # Respuesta exitosa




@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users;')  # Cambia por tu tabla
    users = cur.fetchall()  # Obtén todos los registros
    cur.close()
    conn.close()
    
    return render_template('index.html', users=users)  # Pasa los usuarios al template



# Ejemplo de ruta para obtener datos de la base de datos
@app.route('/data')
def data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users;')  # Cambia por tu tabla
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

# Resto de las rutas...
@app.route('/add_users')
def add_users():
    users = [
        ('Juan Pérez', 'juan.perez@example.com', 'password123'),
        ('Ana Gómez', 'ana.gomez@example.com', 'mypassword'),
        ('Luis Fernández', 'luis.fernandez@example.com', 'securepass'),
        ('María López', 'maria.lopez@example.com', '12345678'),
        ('Carlos Sánchez', 'carlos.sanchez@example.com', 'passw0rd')
    ]

    conn = get_db_connection()
    cur = conn.cursor()

    for user in users:
        cur.execute('INSERT INTO Users (User, Email, Password) VALUES (%s, %s, %s)', user)

    conn.commit()  # Asegúrate de hacer commit para guardar los cambios
    cur.close()
    conn.close()

    return "Usuarios añadidos exitosamente."


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
