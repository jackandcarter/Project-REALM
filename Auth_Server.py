from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt  # Add bcrypt for password hashing
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'administrator'
app.config['MYSQL_DB'] = 'Auth_server'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

# Auth server route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE Username = %s', (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8')):
        # Update user's last login IP and set online status
        update_last_login_ip(username, request.remote_addr)
        update_user_status(username, True)

        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})

# Auth server route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    conn = mysql.connection
    cursor = conn.cursor()

    # Check if the username is already taken
    cursor.execute('SELECT * FROM Users WHERE Username = %s', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({'status': 'error', 'message': 'Username already taken'})
    else:
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert new user into the database
        cursor.execute(
            'INSERT INTO Users (Username, Password, PlayerID, AdminLevel, SubscriptionType, Email) VALUES (%s, %s, %s, %s, %s, %s)',
            (username, hashed_password, generate_player_id(), 0, 'Free', email))

        conn.commit()

        return jsonify({'status': 'success', 'message': 'Registration successful'})

# Helper function to update the user's last login IP
def update_last_login_ip(username, ip_address):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('UPDATE Users SET LastIPAddress = %s WHERE Username = %s', (ip_address, username))
    conn.commit()

# Helper function to update the user's online status
def update_user_status(username, online_status):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('UPDATE Users SET IsOnline = %s WHERE Username = %s', (online_status, username))
    conn.commit()

# Helper function to generate a unique player ID
def generate_player_id():
    now = datetime.now()
    return int(now.timestamp())

if __name__ == '__main__':
    app.run(port=5000)
