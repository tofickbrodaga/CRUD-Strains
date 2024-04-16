from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

connection = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    cursor_factory=RealDictCursor
)
connection.autocommit = True

@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.get("/strains")
def get_strains():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM strains")
        strains = cursor.fetchall()
        for strain in strains:
            strain['users'] = get_users_for_strain(strain['id'])
            strain['experiments'] = get_experiments_for_strain(strain['id'])
    return jsonify(strains)

def get_users_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE strain_id = %s", (strain_id,))
        users = cursor.fetchall()
    return users

def get_experiments_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM experiments WHERE strain_id = %s", (strain_id,))
        experiments = cursor.fetchall()
    return experiments


@app.post("/strains/create")
def create_strain():
    data = request.json
    name = data['name']
    creation_date = data['creation_date']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO strains (name, creation_date) VALUES (%s, %s) RETURNING id", (name, creation_date))
        new_id = cursor.fetchone()['id']
    return jsonify({"id": new_id, "name": name, "creation_date": creation_date})

@app.put("/strains/update/<int:strain_id>")
def update_strain(strain_id):
    data = request.json
    name = data['name']
    creation_date = data['creation_date']
    with connection.cursor() as cursor:
        cursor.execute("UPDATE strains SET name = %s, creation_date = %s WHERE id = %s", (name, creation_date, strain_id))
    return '', 204

@app.delete("/strains/delete/<int:strain_id>")
def delete_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM strains WHERE id = %s", (strain_id,))
    return '', 204

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
