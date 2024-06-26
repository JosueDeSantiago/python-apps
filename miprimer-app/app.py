from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return '<h1>Mi aplicación de Flask!</h1>'

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
       name = request.form['name']
       conn = get_db_connection()
       conn.execute('INSERT INTO data (name) VALUES (?)', (name,))
       conn.commit()
       conn.close()
       return jsonify({'name': name})
    else:
       conn = get_db_connection()
       data = conn.execute('SELECT * FROM data order by name asc').fetchall()
       conn.close()
       html = '<h1> Mi lista de nombres </h1>'
       html += '<ul>'
       for row in data:
           html += f'<li>{row["name"]}</li>'
       html += '</ul>'
       return html

if __name__ == '__main__':
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, name TEXT)')
    conn.close()
    app.run(debug=True, host='0.0.0.0')