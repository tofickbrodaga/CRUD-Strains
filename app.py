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
    return '<p>Welcome to the site with experiments!</p>'


@app.get('/strains')
def get_strains():
    query = """
    WITH strains_with_users AS (
        SELECT s.*, json_agg(u.*) AS users
        FROM strains s
        LEFT JOIN user_strains us ON s.id = us.strain_id
        LEFT JOIN users u ON us.user_id = u.id
        GROUP BY s.id
    )
    SELECT jsonb_build_object(
               'id', id,
               'strain_name', strain_name,
               'users', users
           ) AS strain
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

    query = SQL("""
        INSERT INTO strains (strain_name)
        VALUES ({strain_name})
        RETURNING id
    """).format(strain_name=Literal(strain_name))

    with connection.cursor() as cursor:
        cursor.execute(query)
        new_id = cursor.fetchone()['id']

    return jsonify({'id': new_id, 'strain_name': strain_name})


@app.put('/strains/update/<strain_name>')
def update_strain(strain_name):
    data = request.json
    new_creation_date = data['creation_date']

    query = SQL("""
        UPDATE strains
        SET creation_date = {new_creation_date}
        WHERE strain_name = {strain_name}
    """).format(new_creation_date=Literal(new_creation_date), strain_name=Literal(strain_name))

    with connection.cursor() as cursor:
        cursor.execute(query)

    return '', 204


@app.delete('/strains/delete/<strain_name>')
def delete_strain(strain_name):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM strains WHERE strain_name = %s', (strain_name,))
    return '', 204


if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_PORT'))
