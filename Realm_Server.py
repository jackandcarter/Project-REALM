from flask import Flask, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL


app = Flask(__name__)
CORS(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'administrator'
app.config['MYSQL_DATABASE_DB'] = 'Realm_server'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

# Realm server route for retrieving realm list
@app.route('/realm/list', methods=['GET'])
def get_realm_list():
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM Realms')
    realms = cursor.fetchall()

    realm_list = []
    for realm in realms:
        realm_info = {
            'realmID': realm[0],
            'realmName': realm[1],
            'realmType': realm[2],
            'maxCharacters': realm[3]
        }
        realm_list.append(realm_info)

    return jsonify(realm_list)

if __name__ == '__main__':
    app.run(port=5001)
