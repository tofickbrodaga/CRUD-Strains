from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

connection = psycopg2.connect(
    host='localhost',
    port=os.getenv('POSTGRES_PORT'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    cursor_factory=RealDictCursor
)
connection.autocommit = True


@app.get('/')
def hello_world():
    return '<p>Welcome to the site with experiments!</p>'


def get_users_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user_strains WHERE strain_id = (select id from strains where strain_name = %s)', (strain_id,))
        users = cursor.fetchall()
    return users


def get_experiments_for_strain(strain_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, start_date, end_date, growth_environment, results FROM experiments WHERE strain_name = %s', (strain_id,))
        experiments = cursor.fetchall()
        return experiments


@app.get('/experiments')
def get_experiments():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM experiments')
        experiments = cursor.fetchall()
        for experiment in experiments:
            strain_name = experiment['strain_name']
            experiment['users'] = get_users_for_strain(strain_name)
            experiment['start_date'] = experiment['start_date'].isoformat()
            experiment['end_date'] = experiment['end_date'].isoformat()
            experiment['experiments'] = get_experiments_for_strain(strain_name)
    return jsonify(experiments)


@app.post('/experiments/create')
def create_experiment():
    data = request.json
    strain_id = data['strain_name']
    start_date = data['start_date']
    end_date = data['end_date']
    growthenvironment = data['growth_environment']
    results = data['results']
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO experiments (strain_name, start_date, end_date, growth_environment, results) VALUES (%s, %s, %s, %s, %s) RETURNING id', (strain_id, start_date, end_date, growthenvironment, results))
        new_id = cursor.fetchone()['id']
    return jsonify({'id': new_id, 'strain_id': strain_id, 'start_date': start_date, 'end_date': end_date, 'growth_environment': growthenvironment, 'results': results})


@app.put('/experiments/update/<id>')
def update_experiment(id):
    data = request.json
    strain_name = data['strain_name']
    start_date = data['start_date']
    end_date = data['end_date']
    growthenvironment = data['growth_environment']
    results = data['results']
    with connection.cursor() as cursor:
        cursor.execute('UPDATE experiments SET strain_name = %s, start_date = %s, end_date = %s, growth_environment = %s, results = %s WHERE id = %s', (strain_name, start_date, end_date, growthenvironment, results, id))
    return '', 204


@app.delete('/experiments/delete/<id>')
def delete_experiment(id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM experiments WHERE id = %s', (id,))
    return '', 204


if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
