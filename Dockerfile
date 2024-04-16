FROM python:3.11.5

WORKDIR /CRUD-Strains

COPY app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt