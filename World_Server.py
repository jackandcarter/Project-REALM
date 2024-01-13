from flask import Flask, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'administrator'
app.config['MYSQL_DB'] = 'World_server'
app.config['MYSQL_PORT'] = 3306  # MySQL default port

mysql = MySQL(app)

# Routes for level progression, classes, items, building materials, armor, and spells
@app.route('/level/progression')
def get_level_progression():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM level_progression")
    level_progression_data = cur.fetchall()
    cur.close()
    return jsonify({"level_progression": level_progression_data})

@app.route('/classes')
def get_classes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM classes")
    classes_data = cur.fetchall()
    cur.close()
    return jsonify({"classes": classes_data})

@app.route('/items')
def get_items():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    items_data = cur.fetchall()
    cur.close()
    return jsonify({"items": items_data})

@app.route('/building/materials')
def get_building_materials():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM building_materials")
    building_materials_data = cur.fetchall()
    cur.close()
    return jsonify({"building_materials": building_materials_data})

# Additional routes for armor and spells
@app.route('/armor')
def get_armor():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM armor")
    armor_data = cur.fetchall()
    cur.close()
    return jsonify({"armor": armor_data})

@app.route('/spells')
def get_spells():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spells")
    spells_data = cur.fetchall()
    cur.close()
    return jsonify({"spells": spells_data})

# Run the Flask app
if __name__ == '__main__':
    app.run(port=5002)
