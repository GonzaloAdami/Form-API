from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import mysql.connector

app = Flask(__name__)
CORS(app)


def get_db_connection():
    conn = mysql.connector.connect(
        host='bithey6ubcu8kcihev1e-mysql.services.clever-cloud.com',
        user='uakeyenhcaalsi1w',
        password='NfnTn35YPwpo08FaM4Dd',
        database='bithey6ubcu8kcihev1e',
        port=3306  
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def handle_form():
    data = request.get_json()  
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Todos los campos son obligatorios!'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('INSERT INTO Users (User, Email, Password) VALUES (%s, %s, %s)', 
                    (username, email, password))
        conn.commit()  
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Usuario agregado exitosamente!'}), 201 

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Correo y contraseña son obligatorios!'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('SELECT * FROM Users WHERE Email = %s AND Password = %s', (email, password))
        user = cur.fetchone()  
        
        if user:
            return jsonify({'message': 'Login exitoso!', 'user': user}), 200  
        else:
            return jsonify({'error': 'Correo o contraseña incorrectos!'}), 401  
        
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500  
    finally:
        cur.close()
        conn.close()

@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users;')  
    users = cur.fetchall()  
    cur.close()
    conn.close()
    
    return render_template('index.html', users=users)  


@app.route('/data')
def data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users;')  
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

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

    conn.commit() 
    cur.close()
    conn.close()

    return "Usuarios añadidos exitosamente."
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
