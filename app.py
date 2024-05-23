from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL, Literal
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

@app.get('/')
def hello_world():
    return '<p>Welcome to the site with strains!</p>'

@app.get('/strains')
def get_strains():
    query = """
    WITH strains_with_users AS (
        SELECT s.*, json_agg(u.*) AS users
        FROM strains_exp.strains s
        LEFT JOIN strains_exp.user_strains us ON s.id = us.strain_id
        LEFT JOIN strains_exp.users u ON us.user_id = u.id
        GROUP BY s.id
    )
    SELECT id, strain_name, creation_date, users
    FROM strains_with_users;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        strains = cursor.fetchall()

    return jsonify(strains)

@app.post('/strains/create')
def create_strain():
    data = request.json
    strain_name = data['strain_name']
    creation_date = data['creation_date']

    query = SQL("""
        INSERT INTO strains_exp.strains (strain_name, creation_date)
        VALUES ({strain_name}, {creation_date})
        RETURNING id
    """).format(strain_name=Literal(strain_name), creation_date=Literal(creation_date))

    with connection.cursor() as cursor:
        cursor.execute(query)
        new_id = cursor.fetchone()['id']

    return jsonify({'id': new_id, 'strain_name': strain_name, 'creation_date': creation_date})

@app.put('/strains/update/<strain_name>')
def update_strain(strain_name):
    data = request.json
    new_creation_date = data['creation_date']

    query = SQL("""
        UPDATE strains_exp.strains
        SET creation_date = {new_creation_date}
        WHERE strain_name = {strain_name}
    """).format(new_creation_date=Literal(new_creation_date), strain_name=Literal(strain_name))

    with connection.cursor() as cursor:
        cursor.execute(query)

    return '', 204


@app.delete('/strains/delete/<strain_name>')
def delete_strain(strain_name):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM strains_exp.strains WHERE strain_name = %s', (strain_name,))
    return '', 204


@app.get('/strains/find_by_name')
def get_strain_by_name():
    strain_name = request.args.get('strain_name')
    
    if not strain_name:
        return jsonify({'error': 'strain_name parameter is required'}), 400

    query = SQL("""
        SELECT id, strain_name, creation_date
        FROM strains_exp.strains
        WHERE strain_name ILIKE {strain_name}
    """).format(strain_name=Literal('%' + strain_name + '%'))

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    return jsonify(result)


@app.route('/strains/find_by_creation_date')
def get_strain_by_creation_date():
    creation_date = request.args.get('creation_date')

    query = SQL("""
        SELECT id, strain_name, creation_date
        FROM strains_exp.strains
        WHERE creation_date = %s
    """)

    with connection.cursor() as cursor:
        cursor.execute(query, (creation_date,))
        result = cursor.fetchall()

    return jsonify(result)


if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
