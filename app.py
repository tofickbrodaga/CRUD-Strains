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

@app.post("/strains/create")
def create_strain():
    data = request.json
    user_login = data['user_login']
    strain_name = data['strain_name']
    creation_date = data['creation_date']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO strains (user_login, strain_name, creation_date) VALUES (%s, %s, %s) RETURNING id", (user_login, strain_name, creation_date))
        new_id = cursor.fetchone()['id']
    return jsonify({"id": new_id, "strain_name": strain_name, "creation_date": creation_date})

@app.get("/experiments")
def get_experiments():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM experiments")
        experiments = cursor.fetchall()
        for experiment in experiments:
            strain_id = experiment['strain_id']
            experiment['strain'] = get_users_for_strain(strain_id)
            experiment['start_date'] = experiment['start_date'].isoformat()
            experiment['end_date'] = experiment['end_date'].isoformat()
            experiment['experiments'] = get_experiments_for_strain(strain_id)
    return jsonify(experiments)


def get_users_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE strain_id = %s", (strain_id,))
        users = cursor.fetchall()
    return users

def get_experiments_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, start_date, end_date, growthenvironment, results FROM experiments WHERE strain_id = %s", (strain_id,))
        experiments = cursor.fetchall()
        return experiments


@app.post("/strains/create")
def create_strain():
    data = request.json
    name = data['strain_name']
    creation_date = data['creation_date']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO strains (strain_name, creation_date) VALUES (%s, %s) RETURNING id", (name, creation_date))
        new_id = cursor.fetchone()['id']
    return jsonify({"id": new_id, "strain_name": name, "creation_date": creation_date})

@app.put("/strains/update/<int:strain_id>")
def update_strain(strain_id):
    data = request.json
    name = data['name']
    creation_date = data['creation_date']
    with connection.cursor() as cursor:
        cursor.execute("UPDATE strains SET strain_name = %s, creation_date = %s WHERE id = %s", (name, creation_date, strain_id))
    return '', 204

@app.delete("/strains/delete/<uuid:strain_id>")
def delete_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM strains WHERE id = %s", (strain_id,))
    return '', 204

@app.post("/experiments/create")
def create_experiment():
    data = request.json
    strain_id = data['strain_id']
    start_date = data['start_date']
    end_date = data['end_date']
    growthenvironment = data['growthenvironment']
    results = data['results']
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO experiments (strain_id, start_date, end_date, growthenvironment, results) VALUES (%s, %s, %s, %s, %s) RETURNING id", (strain_id, start_date, end_date, growthenvironment, results))
        new_id = cursor.fetchone()['id']
    return jsonify({"id": new_id, "strain_id": strain_id, "start_date": start_date, "end_date": end_date, "growthenvironment": growthenvironment, "results": results})

@app.put("/experiments/update/<uuid:experiment_id>")
def update_experiment(experiment_id):
    data = request.json
    strain_id = data['strain_id']
    start_date = data['start_date']
    end_date = data['end_date']
    growthenvironment = data['growthenvironment']
    results = data['results']
    with connection.cursor() as cursor:
        cursor.execute("UPDATE experiments SET strain_id = %s, start_date = %s, end_date = %s, growthenvironment = %s, results = %s WHERE id = %s", (strain_id, start_date, end_date, growthenvironment, results, experiment_id))
    return '', 204

@app.delete("/experiments/delete/<uuid:experiment_id>")
def delete_experiment(experiment_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM experiments WHERE id = %s", (experiment_id,))
    return '', 204

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
