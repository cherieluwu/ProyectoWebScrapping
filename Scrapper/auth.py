from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import re

# Crear la instancia de Flask
app = Flask(__name__)
# Configurar CORS correctamente
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Tu usuario de MySQL
        password="",  # Tu contraseña de MySQL
        database="comparador_precios"
    )

# Validación de email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    # Manejar preflight request
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Validaciones
    if not all([email, username, password]):
        return jsonify({'error': 'Todos los campos son requeridos'}), 400
    
    if not is_valid_email(email):
        return jsonify({'error': 'Email inválido'}), 400

    # Hash de la contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar si el usuario o email ya existen
        cursor.execute("SELECT * FROM usuarios WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            return jsonify({'error': 'Usuario o email ya existe'}), 400

        # Insertar nuevo usuario
        cursor.execute(
            "INSERT INTO usuarios (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        conn.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    # Manejar preflight request
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar usuario
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Login exitoso', 'username': user['username']}), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close() 