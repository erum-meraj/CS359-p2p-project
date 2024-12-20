# server.py
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import sqlite3
import bcrypt
import os
import logging
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)
api = Api(app)

DATABASE = 'database.db'
db_lock = Lock()

# Initialize Database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        # Users table
        c.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Files table
        c.execute('''
            CREATE TABLE files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                shared_by INTEGER,
                ip_address TEXT,
                port INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(shared_by) REFERENCES users(user_id)
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database initialized with users and files tables.")

# User Registration Resource
class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logging.warning("Registration attempt with missing username or password.")
            return {'message': 'Username and password are required.'}, 400

        # Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            with db_lock:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed))
                user_id = c.lastrowid
                conn.commit()
                conn.close()
            logging.info(f"User '{username}' registered successfully with user_id {user_id}.")
            return {'message': 'User registered successfully.', 'user_id': user_id}, 201
        except sqlite3.IntegrityError:
            logging.warning(f"Registration failed: Username '{username}' already exists.")
            return {'message': 'Username already exists.'}, 400
        except Exception as e:
            logging.error(f"Registration error: {e}")
            return {'message': 'Internal server error.'}, 500

# User Login Resource
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logging.warning("Login attempt with missing username or password.")
            return {'message': 'Username and password are required.'}, 400

        try:
            with db_lock:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                c.execute("SELECT user_id, password_hash FROM users WHERE username = ?", (username,))
                user = c.fetchone()
                conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                logging.info(f"User '{username}' logged in successfully with user_id {user[0]}.")
                return {'message': 'Login successful.', 'user_id': user[0]}, 200
            else:
                logging.warning(f"Login failed for username '{username}'. Invalid credentials.")
                return {'message': 'Invalid credentials.'}, 401
        except Exception as e:
            logging.error(f"Login error: {e}")
            return {'message': 'Internal server error.'}, 500

# File Registration Resource
class RegisterFile(Resource):
    def post(self):
        data = request.get_json()
        file_name = data.get('file_name')
        file_size = data.get('file_size')
        file_type = data.get('file_type')
        shared_by = data.get('shared_by')
        ip_address = data.get('ip_address')
        port = data.get('port')

        if not all([file_name, shared_by, ip_address, port]):
            logging.warning("File registration attempt with missing fields.")
            return {'message': 'File name, shared_by (user_id), ip_address, and port are required.'}, 400

        try:
            with db_lock:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO files (file_name, file_size, file_type, shared_by, ip_address, port)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (file_name, file_size, file_type, shared_by, ip_address, port))
                conn.commit()
                conn.close()
            logging.info(f"File '{file_name}' registered by user_id {shared_by} with IP {ip_address}:{port}.")
            return {'message': 'File registered successfully.'}, 201
        except Exception as e:
            logging.error(f"File registration error: {e}")
            return {'message': 'Internal server error.'}, 500

# Search Files Resource
class SearchFiles(Resource):
    def get(self):
        query = request.args.get('query', '')
        file_type = request.args.get('type', '')

        try:
            with db_lock:
                conn = sqlite3.connect(DATABASE)
                c = conn.cursor()
                sql = """
                    SELECT f.file_id, f.file_name, f.file_size, f.file_type, u.username, f.ip_address, f.port
                    FROM files f
                    JOIN users u ON f.shared_by = u.user_id
                    WHERE f.file_name LIKE ?
                """
                params = ('%' + query + '%',)

                if file_type:
                    sql += " AND f.file_type = ?"
                    params += (file_type,)

                c.execute(sql, params)
                results = c.fetchall()
                conn.close()

            files = []
            for row in results:
                files.append({
                    'file_id': row[0],
                    'file_name': row[1],
                    'file_size': row[2],
                    'file_type': row[3],
                    'shared_by': row[4],
                    'ip_address': row[5],
                    'port': row[6]
                })

            logging.info(f"Search performed with query='{query}' and type='{file_type}'. Found {len(files)} files.")
            return {'files': files}, 200
        except Exception as e:
            logging.error(f"Search error: {e}")
            return {'message': 'Internal server error.'}, 500

# Add Resources to API
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(RegisterFile, '/register_file')
api.add_resource(SearchFiles, '/search')

if __name__ == '__main__':
    init_db()
    logging.info("Starting the server...")
    app.run(host='0.0.0.0', port=5000)
